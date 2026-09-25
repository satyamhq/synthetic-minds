"""
Knowledge Graph Construction Service
Builds standalone knowledge graphs using Zep Cloud API.
"""

import hashlib
import uuid
import time
import threading
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass

from zep_cloud import BatchAddItem, EntityEdgeSourceTarget, NotFoundError

from ..config import Config
from ..models.task import TaskManager, TaskStatus
from ..utils.zep_paging import fetch_all_nodes, fetch_all_edges
from ..utils.ontology import (
    MAX_ONTOLOGY_TYPES,
    RESERVED_ONTOLOGY_ATTRIBUTE_NAMES,
    normalize_ontology_attributes,
    normalize_ontology_source_targets,
)
from ..utils.zep import (
    ZEP_INGESTION_WAIT_TIMEOUT_SECONDS,
    call_zep_read_with_retry,
    get_zep_client,
    is_retryable_zep_error,
)
from .text_processor import TextProcessor
from ..utils.locale import t, get_locale, set_locale


@dataclass
class GraphInfo:
    """Graph summary information."""
    graph_id: str
    node_count: int
    edge_count: int
    entity_types: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "graph_id": self.graph_id,
            "node_count": self.node_count,
            "edge_count": self.edge_count,
            "entity_types": self.entity_types,
        }


@dataclass(frozen=True)
class BatchSubmission:
    """Durable identity for one Zep Batch API ingestion operation."""

    batch_id: str
    operation_id: str
    episode_uuids: List[str]
    item_count: int


class GraphBuilderService:
    """
    Knowledge Graph Construction Service
    Manages Zep Cloud graph creation, ontology application, and data ingestion.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or Config.ZEP_API_KEY
        if not self.api_key:
            raise ValueError("ZEP_API_KEY is not configured")
        
        self.client = get_zep_client(self.api_key)
        self.task_manager = TaskManager()
    
    def build_graph_async(
        self,
        text: str,
        ontology: Dict[str, Any],
        graph_name: str = "Synthetic Minds Graph",
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        batch_size: int = 350
    ) -> str:
        """
        Asynchronously construct knowledge graph in a background thread.
        
        Args:
            text: Input document text
            ontology: Ontology definition schema
            graph_name: Graph name
            chunk_size: Text chunk size
            chunk_overlap: Text chunk overlap
            batch_size: Chunks per batch
            
        Returns:
            Task ID string
        """
        task_id = self.task_manager.create_task(
            task_type="graph_build",
            metadata={
                "graph_name": graph_name,
                "chunk_size": chunk_size,
                "text_length": len(text),
            }
        )
        
        current_locale = get_locale()

        thread = threading.Thread(
            target=self._build_graph_worker,
            args=(task_id, text, ontology, graph_name, chunk_size, chunk_overlap, batch_size, current_locale)
        )
        thread.daemon = True
        thread.start()
        
        return task_id
    
    def _build_graph_worker(
        self,
        task_id: str,
        text: str,
        ontology: Dict[str, Any],
        graph_name: str,
        chunk_size: int,
        chunk_overlap: int,
        batch_size: int,
        locale: str = 'en'
    ):
        """Worker thread for graph construction."""
        set_locale(locale)
        try:
            self.task_manager.update_task(
                task_id,
                status=TaskStatus.PROCESSING,
                progress=5,
                message=t('progress.startBuildingGraph')
            )
            
            chunks = TextProcessor.split_text(text, chunk_size, chunk_overlap)
            self.validate_batch_chunks(chunks, batch_size=batch_size)
            total_chunks = len(chunks)

            # 1. Create graph
            graph_id = self.create_graph(graph_name)
            self.task_manager.update_task(
                task_id,
                progress=10,
                message=t('progress.graphCreated', graphId=graph_id)
            )
            
            # 2. Set ontology
            self.set_ontology(graph_id, ontology)
            self.task_manager.update_task(
                task_id,
                progress=15,
                message=t('progress.ontologySet')
            )
            
            # 3. Document chunking completed and verified
            self.task_manager.update_task(
                task_id,
                progress=20,
                message=t('progress.textSplit', count=total_chunks)
            )
            
            # 4. Ingest text batches
            submission = self.add_text_batches(
                graph_id, chunks, batch_size,
                lambda msg, prog: self.task_manager.update_task(
                    task_id,
                    progress=20 + int(prog * 0.4),  # 20-60%
                    message=msg
                )
            )
            
            # 5. Wait for Zep processing to complete
            self.task_manager.update_task(
                task_id,
                progress=60,
                message=t('progress.waitingZepProcess')
            )
            
            self._wait_for_batch(
                submission,
                lambda msg, prog: self.task_manager.update_task(
                    task_id,
                    progress=60 + int(prog * 0.3),  # 60-90%
                    message=msg
                )
            )
            
            # 6. Retrieve graph summary
            self.task_manager.update_task(
                task_id,
                progress=90,
                message=t('progress.fetchingGraphInfo')
            )
            
            graph_info = self._get_graph_info(graph_id)
            
            # Completed
            self.task_manager.complete_task(task_id, {
                "graph_id": graph_id,
                "graph_info": graph_info.to_dict(),
                "chunks_processed": total_chunks,
            })
            
        except Exception as e:
            import traceback
            error_msg = f"{str(e)}\n{traceback.format_exc()}"
            self.task_manager.fail_task(task_id, error_msg)
    
    def create_graph(
        self,
        name: str = "Synthetic Minds Graph",
        graph_id: Optional[str] = None,
        graph_id_callback: Optional[Callable[[str], None]] = None,
    ) -> str:
        """Create new graph on Zep Cloud with identity persistence and timeout reconciliation."""
        if not graph_id:
            import uuid
            graph_id = f"graph_{uuid.uuid4().hex[:12]}"

        if graph_id_callback:
            graph_id_callback(graph_id)

        try:
            graph = self.client.graph.create(graph_id=graph_id, name=name)
        except Exception as exc:
            if not is_retryable_zep_error(exc) and not isinstance(exc, (TimeoutError, Exception)):
                raise
            try:
                graph = call_zep_read_with_retry(
                    lambda: self.client.graph.get(graph_id),
                    operation_name=f"reconcile graph get {graph_id}",
                )
            except Exception:
                raise exc

        return getattr(graph, 'graph_id', None) or getattr(graph, 'uuid', graph_id)
    
    @classmethod
    def build_operation_id(cls, graph_id: str, chunks: List[str]) -> str:
        """Compute durable, content-derived operation hash."""
        hasher = hashlib.sha256()
        hasher.update(graph_id.encode("utf-8"))
        hasher.update(str(len(chunks)).encode("utf-8"))
        for chunk in chunks:
            hasher.update(chunk.encode("utf-8"))
        return hasher.hexdigest()

    @classmethod
    def build_episode_uuids(cls, operation_id: str, count: int) -> List[str]:
        """Derive deterministic UUIDs for episodes in a batch."""
        base_namespace = uuid.UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")
        op_namespace = uuid.uuid5(base_namespace, operation_id)
        return [str(uuid.uuid5(op_namespace, f"episode:{i}")) for i in range(count)]

    @classmethod
    def validate_batch_chunks(cls, chunks: List[str], batch_size: int = 350) -> None:
        """Validate batch chunks limits."""
        if not chunks:
            raise ValueError("Text contains no valid chunks after splitting")
        if len(chunks) > batch_size:
            raise ValueError(
                f"Payload produces {len(chunks)} chunks, exceeding the batch "
                f"limit of {batch_size}. Increase chunk_size to fit in one batch."
            )

    def _reconcile_created_batch(
        self,
        *,
        graph_id: str,
        operation_id: str,
        max_attempts: int = 3,
    ) -> Any | None:
        """Find server-created batch after ambiguous creation reply."""
        for attempt in range(1, max_attempts + 1):
            matches: List[Any] = []
            cursor: int | None = None
            seen_cursors: set[int] = set()
            while True:
                page = call_zep_read_with_retry(
                    lambda: self.client.batch.list(limit=100, cursor=cursor),
                    operation_name=f"reconcile batch create {operation_id}",
                )
                for batch in getattr(page, "batches", None) or []:
                    metadata = getattr(batch, "metadata", None) or {}
                    if (
                        metadata.get("synthetic_minds_operation_id") == operation_id
                        and metadata.get("graph_id") == graph_id
                    ):
                        matches.append(batch)
                next_cursor = getattr(page, "next_cursor", None)
                if next_cursor is None:
                    break
                if next_cursor == cursor or next_cursor in seen_cursors:
                    raise RuntimeError("Zep batch list cursor did not advance")
                seen_cursors.add(next_cursor)
                cursor = next_cursor

            if len(matches) > 1:
                raise RuntimeError(
                    f"Multiple Zep batches match operation {operation_id}; refusing ambiguity"
                )
            if matches:
                return matches[0]
            if attempt < max_attempts:
                time.sleep(attempt)
        return None
    
    def set_ontology(self, graph_id: str, ontology: Dict[str, Any]):
        """Apply ontology definition schema to graph."""
        import warnings
        from typing import Optional
        from pydantic import Field
        from zep_cloud.external_clients.ontology import EntityModel, EntityText, EdgeModel
        
        warnings.filterwarnings('ignore', category=UserWarning, module='pydantic')
        
        def safe_attr_name(attr_name: str) -> str:
            """Convert reserved keywords to safe names."""
            if attr_name.lower() in RESERVED_ONTOLOGY_ATTRIBUTE_NAMES:
                return f"entity_{attr_name}"
            return attr_name
        
        # Dynamically create entity types
        entity_types = {}
        for entity_def in ontology.get("entity_types", [])[:MAX_ONTOLOGY_TYPES]:
            name = entity_def["name"]
            description = entity_def.get("description", f"A {name} entity.")
            
            attrs = {"__doc__": description}
            annotations = {}
            
            for normalized in normalize_ontology_attributes(
                entity_def.get("attributes", [])
            ):
                attr_name = safe_attr_name(normalized["name"])
                attr_desc = normalized["description"]
                attrs[attr_name] = Field(description=attr_desc, default=None)
                annotations[attr_name] = Optional[EntityText]
            
            attrs["__annotations__"] = annotations
            
            entity_class = type(name, (EntityModel,), attrs)
            entity_class.__doc__ = description
            entity_types[name] = entity_class
        
        # Dynamically create edge types
        edge_definitions = {}
        for edge_def in ontology.get("edge_types", [])[:MAX_ONTOLOGY_TYPES]:
            name = edge_def["name"]
            description = edge_def.get("description", f"A {name} relationship.")
            
            attrs = {"__doc__": description}
            annotations = {}
            
            for normalized in normalize_ontology_attributes(
                edge_def.get("attributes", [])
            ):
                attr_name = safe_attr_name(normalized["name"])
                attr_desc = normalized["description"]
                attrs[attr_name] = Field(description=attr_desc, default=None)
                annotations[attr_name] = Optional[str]
            
            attrs["__annotations__"] = annotations
            
            class_name = ''.join(word.capitalize() for word in name.split('_'))
            edge_class = type(class_name, (EdgeModel,), attrs)
            edge_class.__doc__ = description
            
            source_targets = []
            for st in normalize_ontology_source_targets(
                edge_def.get("source_targets", [])
            ):
                source_targets.append(
                    EntityEdgeSourceTarget(
                        source=st.get("source", "Entity"),
                        target=st.get("target", "Entity")
                    )
                )
            
            if source_targets:
                edge_definitions[name] = (edge_class, source_targets)
        
        if entity_types or edge_definitions:
            self.client.graph.set_ontology(
                graph_ids=[graph_id],
                entities=entity_types,
                edges=edge_definitions if edge_definitions else None,
            )
    
    def add_text_batches(
        self,
        graph_id: str,
        chunks: List[str],
        batch_size: int = 350,
        progress_callback: Optional[Callable] = None,
        batch_created_callback: Optional[Callable[[Optional[str], str], None]] = None,
    ) -> BatchSubmission:
        """Submit text chunks in a single validated batch."""
        self.validate_batch_chunks(chunks, batch_size=batch_size)
        operation_id = self.build_operation_id(graph_id, chunks)
        episode_uuids = self.build_episode_uuids(operation_id, len(chunks))

        if batch_created_callback:
            batch_created_callback(None, operation_id)

        if progress_callback:
            progress_callback(t('progress.submittingBatch', count=len(chunks)), 0.2)

        # 1. Create batch
        reconciled_batch = None
        try:
            batch_result = self.client.batch.create(
                metadata={
                    "synthetic_minds_operation_id": operation_id,
                    "graph_id": graph_id,
                    "item_count": len(chunks),
                },
            )
        except Exception as exc:
            if not is_retryable_zep_error(exc) and not isinstance(exc, (TimeoutError, Exception)):
                raise
            reconciled_batch = self._reconcile_created_batch(
                graph_id=graph_id,
                operation_id=operation_id,
            )
            if reconciled_batch is None:
                raise

        batch_id = (
            getattr(reconciled_batch, "batch_id", None)
            or getattr(reconciled_batch, "uuid_", None)
            or getattr(reconciled_batch, "uuid", None)
            if reconciled_batch is not None
            else getattr(batch_result, "batch_id", None)
            or getattr(batch_result, "uuid_", None)
            or getattr(batch_result, "uuid", None)
        )
        if not batch_id:
            raise RuntimeError(f"Zep batch creation returned no batch id for operation {operation_id}")

        batch_id = str(batch_id)
        if batch_created_callback:
            batch_created_callback(batch_id, operation_id)

        items = [
            BatchAddItem(
                data=chunk,
                data_type="text",
                graph_id=graph_id,
                metadata={"sequence_index": i, "operation_id": operation_id},
                source_description="Synthetic Minds source document chunk",
                type="graph_episode",
            )
            for i, chunk in enumerate(chunks)
        ]

        try:
            self.client.batch.add(
                batch_id=batch_id,
                items=items,
            )
        except Exception as exc:
            if not is_retryable_zep_error(exc) and not isinstance(exc, (TimeoutError, Exception)):
                raise
            self._reconcile_added_items(batch_id=batch_id, expected_count=len(items))

        self.client.batch.process(batch_id=batch_id)

        if progress_callback:
            progress_callback(t('progress.batchSubmitted', batchId=batch_id), 1.0)

        return BatchSubmission(
            batch_id=batch_id,
            operation_id=operation_id,
            episode_uuids=episode_uuids,
            item_count=len(items),
        )

    def _reconcile_added_items(
        self,
        batch_id: str,
        expected_count: int,
        max_attempts: int = 3,
    ) -> List[Any]:
        """Verify added items without replaying on ambiguous timeout."""
        for _ in range(max_attempts):
            try:
                res = call_zep_read_with_retry(
                    lambda: self.client.batch.list_items(batch_id=batch_id),
                    operation_name=f"reconcile items {batch_id}",
                )
            except TypeError:
                res = call_zep_read_with_retry(
                    lambda: self.client.batch.list_items(),
                    operation_name=f"reconcile items {batch_id}",
                )
            items = getattr(res, "items", None) or []
            if len(items) >= expected_count:
                return items
            time.sleep(1)
        raise TimeoutError(f"Failed to reconcile items for batch {batch_id}")

    def _wait_for_batch(
        self,
        submission: BatchSubmission,
        progress_callback: Optional[Callable] = None,
        timeout: int = ZEP_INGESTION_WAIT_TIMEOUT_SECONDS,
    ) -> List[str]:
        """Poll Batch API status and return completed episode UUIDs."""
        batch_id = submission.batch_id
        start_time = time.time()
        last_progress_bucket = -1

        if progress_callback:
            progress_callback(t('progress.waitingBatch', batchId=batch_id), 0.0)

        while True:
            elapsed = time.time() - start_time
            if elapsed > timeout:
                raise TimeoutError(
                    f"Zep batch {batch_id} ingestion timed out after {int(elapsed)}s"
                )

            try:
                batch = call_zep_read_with_retry(
                    lambda: self.client.batch.get(batch_id=batch_id),
                    operation_name=f"poll batch {batch_id}",
                )
            except TypeError:
                batch = call_zep_read_with_retry(
                    lambda: self.client.batch.get(uuid_=batch_id) if hasattr(self.client.batch, 'get') else self.client.batch.get(batch_id),
                    operation_name=f"poll batch {batch_id}",
                )

            raw_status = (getattr(batch, "status", None) or "").strip().lower()

            if raw_status in {"succeeded", "completed", "success", "done"}:
                episodes = []
                cursor = None
                seen_cursors = set()
                while True:
                    cur = cursor
                    try:
                        page = call_zep_read_with_retry(
                            lambda: self.client.batch.list_items(batch_id=batch_id, cursor=cur),
                            operation_name=f"list items batch {batch_id}",
                        )
                    except TypeError:
                        page = call_zep_read_with_retry(
                            lambda: self.client.batch.list_items(cursor=cur),
                            operation_name=f"list items batch {batch_id}",
                        )

                    items = getattr(page, "items", None) or []
                    for it in items:
                        ep_uuid = getattr(it, "episode_uuid", None) or getattr(it, "source_uuid", None)
                        if ep_uuid:
                            episodes.append(ep_uuid)

                    next_cursor = getattr(page, "next_cursor", None)
                    if next_cursor is None or next_cursor in seen_cursors:
                        break
                    seen_cursors.add(next_cursor)
                    cursor = next_cursor

                if progress_callback:
                    progress_callback(t('progress.batchCompleted', batchId=batch_id), 1.0)
                return episodes or submission.episode_uuids

            if raw_status in {"failed", "partial", "invalid", "canceled", "error"}:
                error_detail = (
                    getattr(batch, "error", None)
                    or getattr(batch, "error_message", None)
                    or raw_status
                )
                raise RuntimeError(
                    f"Zep batch {batch_id} failed with status {raw_status}: {error_detail}"
                )

            if not raw_status:
                remaining_timeout = max(5, int(timeout - elapsed))
                self._wait_for_episodes(
                    submission.episode_uuids,
                    progress_callback=progress_callback,
                    timeout=remaining_timeout,
                )
                return submission.episode_uuids

            time.sleep(0.1 if timeout <= 2 else 1)

    def _wait_for_episodes(
        self,
        episode_uuids: List[str],
        progress_callback: Optional[Callable] = None,
        timeout: int = ZEP_INGESTION_WAIT_TIMEOUT_SECONDS
    ):
        """Poll episode processed status until complete."""
        if not episode_uuids:
            if progress_callback:
                progress_callback(t('progress.noEpisodesWait'), 1.0)
            return
        
        start_time = time.time()
        pending_episodes = set(episode_uuids)
        completed_count = 0
        total_episodes = len(episode_uuids)
        
        if progress_callback:
            progress_callback(t('progress.waitingEpisodes', count=total_episodes), 0)
        
        while pending_episodes:
            if time.time() - start_time > timeout:
                if progress_callback:
                    progress_callback(
                        t('progress.episodesTimeout', completed=completed_count, total=total_episodes),
                        completed_count / total_episodes
                    )
                raise TimeoutError(
                    f"Zep episode processing timed out with "
                    f"{len(pending_episodes)} episode(s) still pending"
                )
            
            for ep_uuid in list(pending_episodes):
                episode = call_zep_read_with_retry(
                    lambda: self.client.graph.episode.get(uuid_=ep_uuid),
                    operation_name=f"poll episode {ep_uuid}",
                )
                is_processed = getattr(episode, 'processed', False)

                if is_processed:
                    pending_episodes.remove(ep_uuid)
                    completed_count += 1
            
            elapsed = int(time.time() - start_time)
            if progress_callback:
                progress_callback(
                    t('progress.zepProcessing', completed=completed_count, total=total_episodes, pending=len(pending_episodes), elapsed=elapsed),
                    completed_count / total_episodes if total_episodes > 0 else 0
                )
            
            if pending_episodes:
                time.sleep(3)
        
        if progress_callback:
            progress_callback(t('progress.processingComplete', completed=completed_count, total=total_episodes), 1.0)
    
    def _get_graph_info(self, graph_id: str) -> GraphInfo:
        """Fetch graph nodes, edges, and entity types count."""
        nodes = fetch_all_nodes(self.client, graph_id)
        edges = fetch_all_edges(self.client, graph_id)

        entity_types = set()
        for node in nodes:
            if node.labels:
                for label in node.labels:
                    if label not in ["Entity", "Node"]:
                        entity_types.add(label)

        return GraphInfo(
            graph_id=graph_id,
            node_count=len(nodes),
            edge_count=len(edges),
            entity_types=list(entity_types)
        )
    
    def get_graph_data(self, graph_id: str) -> Dict[str, Any]:
        """
        Fetch full graph payload including nodes and edges.
        
        Args:
            graph_id: Graph ID
            
        Returns:
            Dictionary with nodes and edges details
        """
        nodes = fetch_all_nodes(self.client, graph_id)
        edges = fetch_all_edges(self.client, graph_id)

        node_map = {}
        for node in nodes:
            node_map[node.uuid_] = node.name or ""
        
        nodes_data = []
        for node in nodes:
            created_at = getattr(node, 'created_at', None)
            if created_at:
                created_at = str(created_at)
            
            nodes_data.append({
                "uuid": node.uuid_,
                "name": node.name,
                "labels": node.labels or [],
                "summary": node.summary or "",
                "attributes": node.attributes or {},
                "created_at": created_at,
            })
        
        edges_data = []
        for edge in edges:
            created_at = getattr(edge, 'created_at', None)
            valid_at = getattr(edge, 'valid_at', None)
            invalid_at = getattr(edge, 'invalid_at', None)
            expired_at = getattr(edge, 'expired_at', None)
            
            episodes = getattr(edge, 'episodes', None) or getattr(edge, 'episode_ids', None)
            if episodes and not isinstance(episodes, list):
                episodes = [str(episodes)]
            elif episodes:
                episodes = [str(e) for e in episodes]
            
            fact_type = getattr(edge, 'fact_type', None) or edge.name or ""
            
            edges_data.append({
                "uuid": edge.uuid_,
                "name": edge.name or "",
                "fact": edge.fact or "",
                "fact_type": fact_type,
                "source_node_uuid": edge.source_node_uuid,
                "target_node_uuid": edge.target_node_uuid,
                "source_node_name": node_map.get(edge.source_node_uuid, ""),
                "target_node_name": node_map.get(edge.target_node_uuid, ""),
                "attributes": edge.attributes or {},
                "created_at": str(created_at) if created_at else None,
                "valid_at": str(valid_at) if valid_at else None,
                "invalid_at": str(invalid_at) if invalid_at else None,
                "expired_at": str(expired_at) if expired_at else None,
                "episodes": episodes or [],
            })
        
        return {
            "graph_id": graph_id,
            "nodes": nodes_data,
            "edges": edges_data,
            "node_count": len(nodes_data),
            "edge_count": len(edges_data),
        }
    
    def delete_graph(self, graph_id: str):
        """Delete graph from Zep Cloud."""
        self.client.graph.delete(graph_id=graph_id)
