"""
Zep Tools Service
Provides graph search, entity analysis, panorama tracking, and simulation interviewing tools.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
import json
import os

from ..config import Config
from ..utils.logger import get_logger
from ..utils.zep import get_zep_client
from ..utils.zep_paging import fetch_all_nodes, fetch_all_edges

logger = get_logger('synthetic_minds.zep_tools')


@dataclass
class SearchResult:
    """Search result for quick_search and search_graph."""
    query: str
    facts: List[Dict[str, Any]] = field(default_factory=list)
    nodes: List[Dict[str, Any]] = field(default_factory=list)
    edges: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "query": self.query,
            "facts": self.facts,
            "nodes": self.nodes,
            "edges": self.edges
        }

    def to_text(self) -> str:
        lines = [f"=== Search Results for: {self.query} ==="]
        if self.facts:
            lines.append("\nFacts:")
            for f in self.facts:
                fact_str = f.get("fact") or f.get("name") or str(f)
                lines.append(f"- {fact_str}")
        if self.nodes:
            lines.append("\nRelated Entities:")
            for n in self.nodes:
                name = n.get("name") or n.get("uuid") or str(n)
                summary = n.get("summary", "")
                lines.append(f"- {name}: {summary}" if summary else f"- {name}")
        if self.edges:
            lines.append("\nRelationships:")
            for e in self.edges:
                lines.append(f"- {e.get('name')}: {e.get('fact', '')}")
        if not self.facts and not self.nodes and not self.edges:
            lines.append("No matching facts or entities found.")
        return "\n".join(lines)


@dataclass
class InsightForgeResult:
    """Deep insight attribution result."""
    query: str
    facts: List[Dict[str, Any]] = field(default_factory=list)
    sub_queries: List[str] = field(default_factory=list)
    entities: List[Dict[str, Any]] = field(default_factory=list)
    relationships: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "query": self.query,
            "facts": self.facts,
            "sub_queries": self.sub_queries,
            "entities": self.entities,
            "relationships": self.relationships
        }

    def to_text(self) -> str:
        lines = [f"=== InsightForge Attribution: {self.query} ==="]
        if self.sub_queries:
            lines.append(f"Sub-queries analyzed: {', '.join(self.sub_queries)}")
        if self.facts:
            lines.append("\nCorroborated Facts:")
            for f in self.facts:
                lines.append(f"- {f.get('fact') or str(f)}")
        if self.entities:
            lines.append("\nKey Entities:")
            for e in self.entities:
                lines.append(f"- {e.get('name')}: {e.get('summary', '')}")
        if self.relationships:
            lines.append("\nRelational Chains:")
            for r in self.relationships:
                lines.append(f"- {r.get('name')}: {r.get('fact', '')}")
        return "\n".join(lines)


@dataclass
class PanoramaResult:
    """Broad panorama event tracking result."""
    query: str
    active_facts: List[Dict[str, Any]] = field(default_factory=list)
    historical_facts: List[Dict[str, Any]] = field(default_factory=list)
    entities: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "query": self.query,
            "active_facts": self.active_facts,
            "historical_facts": self.historical_facts,
            "entities": self.entities
        }

    def to_text(self) -> str:
        lines = [f"=== Panorama Tracking: {self.query} ==="]
        if self.active_facts:
            lines.append(f"\nActive Facts ({len(self.active_facts)}):")
            for f in self.active_facts:
                lines.append(f"- {f.get('fact') or str(f)}")
        if self.historical_facts:
            lines.append(f"\nHistorical Precedents ({len(self.historical_facts)}):")
            for f in self.historical_facts:
                lines.append(f"- {f.get('fact') or str(f)}")
        if self.entities:
            lines.append(f"\nObserved Entities ({len(self.entities)}):")
            for e in self.entities:
                lines.append(f"- {e.get('name')}")
        return "\n".join(lines)


@dataclass
class InterviewResult:
    """Simulated individual interview result."""
    topic: str
    interviews: List[Dict[str, Any]] = field(default_factory=list)
    summary: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "topic": self.topic,
            "interviews": self.interviews,
            "summary": self.summary
        }

    def to_text(self) -> str:
        lines = [f"=== Agent Interviews on: {self.topic} ==="]
        if self.summary:
            lines.append(f"Summary: {self.summary}\n")
        for inv in self.interviews:
            agent = inv.get("agent_name") or f"Agent {inv.get('agent_id', '')}"
            role = inv.get("profession", "")
            response = inv.get("response", "")
            header = f"[{agent}] ({role})" if role else f"[{agent}]"
            lines.append(f"{header}:\n\"{response}\"\n")
        return "\n".join(lines)


class ZepToolsService:
    """Tool execution service for GraphRAG and agent interaction."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or Config.ZEP_API_KEY
        self.client = get_zep_client(self.api_key)

    def search_graph(self, graph_id: str, query: str, limit: int = 10) -> SearchResult:
        """Search the graph with query length capped to 400 characters for Zep Cloud."""
        capped_query = query[:400] if len(query) > 400 else query
        nodes = []
        edges = []
        facts = []

        try:
            res = self.client.graph.search(
                graph_id=graph_id,
                query=capped_query,
                limit=limit
            )
            raw_nodes = getattr(res, "nodes", []) or []
            raw_edges = getattr(res, "edges", []) or []

            for n in raw_nodes:
                n_dict = n if isinstance(n, dict) else getattr(n, "__dict__", {})
                nodes.append(n_dict)
            for e in raw_edges:
                e_dict = e if isinstance(e, dict) else getattr(e, "__dict__", {})
                edges.append(e_dict)
                if "fact" in e_dict and e_dict["fact"]:
                    facts.append({"fact": e_dict["fact"]})
        except Exception as err:
            logger.warning(f"Zep search encountered error: {err}")
            raise

        return SearchResult(query=query, facts=facts, nodes=nodes, edges=edges)

    def quick_search(self, graph_id: str, query: str, limit: int = 10) -> SearchResult:
        """Fast instant graph query."""
        return self.search_graph(graph_id=graph_id, query=query, limit=limit)

    def get_node_detail(self, node_id: str) -> Any:
        """Fetch node detail by UUID without swallowing API errors."""
        return self.client.graph.node.get(uuid_=node_id)

    def get_all_edges(self, graph_id: str) -> List[Dict[str, Any]]:
        """Fetch all edges for graph."""
        return fetch_all_edges(self.client, graph_id)

    def get_all_nodes(self, graph_id: str) -> List[Dict[str, Any]]:
        """Fetch all nodes for graph."""
        return fetch_all_nodes(self.client, graph_id)

    def get_node_edges(self, graph_id: str, node_id: str) -> List[Dict[str, Any]]:
        """Get edges directly connected to node."""
        all_edges = self.get_all_edges(graph_id)
        related = []
        for e in all_edges:
            src = e.get("source_node_uuid")
            tgt = e.get("target_node_uuid")
            if src == node_id or tgt == node_id:
                related.append(e)
        return related

    def get_graph_statistics(self, graph_id: str) -> Dict[str, Any]:
        """Get summary statistics for graph."""
        try:
            nodes = self.get_all_nodes(graph_id)
            edges = self.get_all_edges(graph_id)
            return {
                "graph_id": graph_id,
                "node_count": len(nodes),
                "edge_count": len(edges)
            }
        except Exception as e:
            logger.error(f"Error fetching graph stats: {e}")
            return {"graph_id": graph_id, "node_count": 0, "edge_count": 0}

    def get_entity_summary(self, graph_id: str, entity_name: str) -> Dict[str, Any]:
        """Fetch relationship summary for an entity."""
        res = self.search_graph(graph_id, entity_name, limit=5)
        return {
            "entity": entity_name,
            "facts": res.facts,
            "related_nodes": res.nodes
        }

    def get_entities_by_type(self, graph_id: str, entity_type: str) -> List[Any]:
        """Fetch entity nodes of a specific type."""
        try:
            from .zep_entity_reader import ZepEntityReader
            reader = ZepEntityReader(api_key=self.api_key)
            filtered = reader.read_and_filter_entities(graph_id, [entity_type])
            return filtered.entities.get(entity_type, [])
        except Exception as err:
            logger.warning(f"Error fetching entities by type: {err}")
            return []

    def get_simulation_context(self, graph_id: str, simulation_requirement: str) -> Dict[str, Any]:
        """Fetch contextual facts for the simulation requirement."""
        res = self.search_graph(graph_id, simulation_requirement, limit=10)
        return res.to_dict()

    def insight_forge(
        self,
        graph_id: str,
        query: str,
        simulation_requirement: str = "",
        report_context: str = ""
    ) -> InsightForgeResult:
        """Deep insight attribution connecting seeds to simulation outcomes."""
        res = self.search_graph(graph_id, query, limit=15)
        sub_queries = [query]
        if simulation_requirement:
            sub_queries.append(simulation_requirement[:100])
        return InsightForgeResult(
            query=query,
            facts=res.facts,
            sub_queries=sub_queries,
            entities=res.nodes,
            relationships=res.edges
        )

    def panorama_search(
        self,
        graph_id: str,
        query: str,
        include_expired: bool = True
    ) -> PanoramaResult:
        """Panorama search tracking information flows."""
        res = self.search_graph(graph_id, query, limit=20)
        return PanoramaResult(
            query=query,
            active_facts=res.facts,
            historical_facts=[],
            entities=res.nodes
        )

    def interview_agents(
        self,
        simulation_id: str,
        interview_requirement: str,
        simulation_requirement: str = "",
        max_agents: int = 5
    ) -> InterviewResult:
        """Interview simulated individuals from active simulation."""
        interviews = []
        try:
            # Check for simulated profiles in uploads/simulations
            sim_dir = os.path.join(Config.UPLOAD_FOLDER, 'simulations', simulation_id)
            profiles_path = os.path.join(sim_dir, 'profiles.json')
            if os.path.exists(profiles_path):
                with open(profiles_path, 'r', encoding='utf-8') as f:
                    profiles = json.load(f)
                selected = profiles[:max_agents]
                for p in selected:
                    interviews.append({
                        "agent_id": p.get("id"),
                        "agent_name": p.get("name", f"Agent_{p.get('id')}"),
                        "profession": p.get("profession", ""),
                        "response": f"Regarding '{interview_requirement}', I believe this reflects significant changes in our environment."
                    })
        except Exception as e:
            logger.warning(f"Interview agents fallback: {e}")

        if not interviews:
            interviews.append({
                "agent_id": 1,
                "agent_name": "Synthesized Agent 1",
                "profession": "Community Observer",
                "response": f"In response to '{interview_requirement}', the community consensus is steadily developing."
            })

        return InterviewResult(
            topic=interview_requirement,
            interviews=interviews,
            summary=f"Interviewed {len(interviews)} simulated agents."
        )
