"""
Simulation Configuration Generator
Uses LLM to automatically generate comprehensive simulation parameters based on requirements, documents, and graph entities.
Enables end-to-end automation without manual parameter configuration.

Employs a phased generation strategy to prevent token overflow:
1. Generate time simulation configuration
2. Generate event and narrative configuration
3. Generate agent activity configurations in batches
4. Generate platform-specific configurations
"""

import json
import math
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field, asdict
from datetime import datetime

from openai import OpenAI

from ..config import Config
from ..utils.logger import get_logger
from ..utils.locale import get_language_instruction, t
from ..utils.openai_chat_compat import create_chat_completion, extract_chat_completion_text
from .zep_entity_reader import EntityNode, ZepEntityReader

logger = get_logger('synthetic_minds.simulation_config')

# Diurnal schedule configuration (reference daily activity pattern)
DIURNAL_SCHEDULE_CONFIG = CHINA_TIMEZONE_CONFIG = {
    # Late night hours (minimal activity)
    "dead_hours": [0, 1, 2, 3, 4, 5],
    # Morning hours (gradual wakeup)
    "morning_hours": [6, 7, 8],
    # Working hours
    "work_hours": [9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
    # Evening peak hours (highest activity)
    "peak_hours": [19, 20, 21, 22],
    # Night hours (declining activity)
    "night_hours": [23],
    # Activity multipliers
    "activity_multipliers": {
        "dead": 0.05,
        "morning": 0.4,
        "work": 0.7,
        "peak": 1.5,
        "night": 0.5
    }
}


@dataclass
class AgentActivityConfig:
    """Activity configuration for an individual Agent"""
    agent_id: int
    entity_uuid: str
    entity_name: str
    entity_type: str
    
    # Activity level (0.0-1.0)
    activity_level: float = 0.5
    
    # Posting and commenting frequencies (expected actions per hour)
    posts_per_hour: float = 1.0
    comments_per_hour: float = 2.0
    
    # Active hours (24-hour clock, 0-23)
    active_hours: List[int] = field(default_factory=lambda: list(range(8, 23)))
    
    # Response latency in simulation minutes
    response_delay_min: int = 5
    response_delay_max: int = 60
    
    # Sentiment bias (-1.0 negative to 1.0 positive)
    sentiment_bias: float = 0.0
    
    # Stance toward topic
    stance: str = "neutral"  # supportive, opposing, neutral, observer
    
    # Influence weighting
    influence_weight: float = 1.0


@dataclass  
class TimeSimulationConfig:
    """Time simulation configuration based on diurnal rhythms"""
    # Total simulation duration in hours
    total_simulation_hours: int = 72
    
    # Simulation minutes per round (accelerates flow of time)
    minutes_per_round: int = 60
    
    # Range of activated agents per hour
    agents_per_hour_min: int = 5
    agents_per_hour_max: int = 20
    
    # Peak activity hours
    peak_hours: List[int] = field(default_factory=lambda: [19, 20, 21, 22])
    peak_activity_multiplier: float = 1.5
    
    # Off-peak hours
    off_peak_hours: List[int] = field(default_factory=lambda: [0, 1, 2, 3, 4, 5])
    off_peak_activity_multiplier: float = 0.05
    
    # Morning hours
    morning_hours: List[int] = field(default_factory=lambda: [6, 7, 8])
    morning_activity_multiplier: float = 0.4
    
    # Working hours
    work_hours: List[int] = field(default_factory=lambda: [9, 10, 11, 12, 13, 14, 15, 16, 17, 18])
    work_activity_multiplier: float = 0.7


@dataclass
class EventConfig:
    """Event configuration"""
    # Initial trigger posts
    initial_posts: List[Dict[str, Any]] = field(default_factory=list)
    
    # Scheduled events triggering at specific points
    scheduled_events: List[Dict[str, Any]] = field(default_factory=list)
    
    # Hot topics keywords
    hot_topics: List[str] = field(default_factory=list)
    
    # Narrative direction description
    narrative_direction: str = ""


@dataclass
class PlatformConfig:
    """Platform-specific configuration"""
    platform: str  # twitter or reddit
    
    # Recommendation algorithm weights
    recency_weight: float = 0.4
    popularity_weight: float = 0.3
    relevance_weight: float = 0.3
    
    # Viral propagation threshold
    viral_threshold: int = 10
    
    # Echo chamber strength
    echo_chamber_strength: float = 0.5


@dataclass
class SimulationParameters:
    """Complete simulation parameters collection"""
    simulation_id: str
    project_id: str
    graph_id: str
    simulation_requirement: str
    
    time_config: TimeSimulationConfig
    agent_configs: List[AgentActivityConfig]
    event_config: EventConfig
    
    twitter_config: Optional[PlatformConfig] = None
    reddit_config: Optional[PlatformConfig] = None
    
    llm_model: str = "gpt-4o"
    llm_base_url: Optional[str] = None
    
    generation_reasoning: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        return {
            "simulation_id": self.simulation_id,
            "project_id": self.project_id,
            "graph_id": self.graph_id,
            "simulation_requirement": self.simulation_requirement,
            "time_config": asdict(self.time_config),
            "agent_configs": [asdict(cfg) for cfg in self.agent_configs],
            "event_config": asdict(self.event_config),
            "twitter_config": asdict(self.twitter_config) if self.twitter_config else None,
            "reddit_config": asdict(self.reddit_config) if self.reddit_config else None,
            "llm_model": self.llm_model,
            "llm_base_url": self.llm_base_url,
            "generation_reasoning": self.generation_reasoning,
            "created_at": self.created_at
        }


class SimulationConfigGenerator:
    """
    Automated Simulation Parameter Generator
    
    Uses LLM to generate realistic simulation parameters based on documents and graph entities.
    """
    
    # Configuration parameters
    AGENTS_PER_BATCH = 15
    MAX_CONTEXT_LENGTH = 12000
    TIME_CONFIG_CONTEXT_LENGTH = 8000
    EVENT_CONFIG_CONTEXT_LENGTH = 8000
    AGENT_CONFIG_CONTEXT_LENGTH = 8000
    
    ENTITIES_PER_TYPE_DISPLAY = 5
    ENTITY_SUMMARY_LENGTH = 80
    AGENT_SUMMARY_LENGTH = 150
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model_name: Optional[str] = None
    ):
        self.api_key = api_key or Config.OPENAI_API_KEY
        self.base_url = base_url
        self.model_name = model_name or Config.OPENAI_MODEL
        
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is not configured")
        
        if self.base_url:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
        else:
            self.client = OpenAI(
                api_key=self.api_key
            )
    
    def generate_parameters(
        self,
        simulation_id: str,
        project_id: str,
        graph_id: str,
        simulation_requirement: str,
        document_text: str,
        entities: List[EntityNode],
        enable_twitter: bool = True,
        enable_reddit: bool = True,
        progress_callback: Optional[Callable[[int, int, str], None]] = None
    ) -> SimulationParameters:
        """
        Generate complete simulation configuration across sequential stages.
        """
        logger.info(f"Starting simulation config generation: simulation_id={simulation_id}, entities={len(entities)}")
        
        num_batches = math.ceil(len(entities) / self.AGENTS_PER_BATCH)
        total_steps = 3 + num_batches
        current_step = 0
        
        def report_progress(step: int, message: str):
            nonlocal current_step
            current_step = step
            if progress_callback:
                progress_callback(step, total_steps, message)
            logger.info(f"[{step}/{total_steps}] {message}")
        
        # 1. Build context
        context = self._build_context(
            simulation_requirement=simulation_requirement,
            document_text=document_text,
            entities=entities
        )
        
        reasoning_parts = []
        
        # ========== Step 1: Time Configuration ==========
        report_progress(1, t('progress.generatingTimeConfig'))
        num_entities = len(entities)
        time_config_result = self._generate_time_config(context, num_entities)
        time_config = self._parse_time_config(time_config_result, num_entities)
        reasoning_parts.append(f"{t('progress.timeConfigLabel')}: {time_config_result.get('reasoning', t('common.success'))}")
        
        # ========== Step 2: Event Configuration ==========
        report_progress(2, t('progress.generatingEventConfig'))
        event_config_result = self._generate_event_config(context, simulation_requirement, entities)
        event_config = self._parse_event_config(event_config_result)
        reasoning_parts.append(f"{t('progress.eventConfigLabel')}: {event_config_result.get('reasoning', t('common.success'))}")
        
        # ========== Step 3-N: Batch Agent Configurations ==========
        all_agent_configs = []
        for batch_idx in range(num_batches):
            start_idx = batch_idx * self.AGENTS_PER_BATCH
            end_idx = min(start_idx + self.AGENTS_PER_BATCH, len(entities))
            batch_entities = entities[start_idx:end_idx]
            
            report_progress(
                3 + batch_idx,
                t('progress.generatingAgentConfig', start=start_idx + 1, end=end_idx, total=len(entities))
            )
            
            batch_configs = self._generate_agent_configs_batch(
                context=context,
                entities=batch_entities,
                start_idx=start_idx,
                simulation_requirement=simulation_requirement
            )
            all_agent_configs.extend(batch_configs)
        
        reasoning_parts.append(t('progress.agentConfigResult', count=len(all_agent_configs)))
        
        # ========== Assign initial post authors ==========
        logger.info("Assigning appropriate author agents for initial posts...")
        event_config = self._assign_initial_post_agents(event_config, all_agent_configs)
        assigned_count = len([p for p in event_config.initial_posts if p.get("poster_agent_id") is not None])
        reasoning_parts.append(t('progress.postAssignResult', count=assigned_count))
        
        # ========== Final Step: Platform Configuration ==========
        report_progress(total_steps, t('progress.generatingPlatformConfig'))
        twitter_config = None
        reddit_config = None
        
        if enable_twitter:
            twitter_config = PlatformConfig(
                platform="twitter",
                recency_weight=0.4,
                popularity_weight=0.3,
                relevance_weight=0.3,
                viral_threshold=10,
                echo_chamber_strength=0.5
            )
        
        if enable_reddit:
            reddit_config = PlatformConfig(
                platform="reddit",
                recency_weight=0.3,
                popularity_weight=0.4,
                relevance_weight=0.3,
                viral_threshold=15,
                echo_chamber_strength=0.6
            )
        
        params = SimulationParameters(
            simulation_id=simulation_id,
            project_id=project_id,
            graph_id=graph_id,
            simulation_requirement=simulation_requirement,
            time_config=time_config,
            agent_configs=all_agent_configs,
            event_config=event_config,
            twitter_config=twitter_config,
            reddit_config=reddit_config,
            llm_model=self.model_name,
            llm_base_url=self.base_url,
            generation_reasoning=" | ".join(reasoning_parts)
        )
        
        logger.info(f"Simulation parameters generated successfully: {len(params.agent_configs)} agent configurations")
        return params
    
    def _build_context(
        self,
        simulation_requirement: str,
        document_text: str,
        entities: List[EntityNode]
    ) -> str:
        """Construct context truncated to max length."""
        entity_summary = self._summarize_entities(entities)
        
        context_parts = [
            f"## Simulation Requirements\n{simulation_requirement}",
            f"\n## Entity Information ({len(entities)} entities)\n{entity_summary}",
        ]
        
        current_length = sum(len(p) for p in context_parts)
        remaining_length = self.MAX_CONTEXT_LENGTH - current_length - 500
        
        if remaining_length > 0 and document_text:
            doc_text = document_text[:remaining_length]
            if len(document_text) > remaining_length:
                doc_text += "\n...(Document truncated)"
            context_parts.append(f"\n## Original Document Content\n{doc_text}")
        
        return "\n".join(context_parts)
    
    def _summarize_entities(self, entities: List[EntityNode]) -> str:
        """Generate entity summary grouped by type."""
        lines = []
        
        by_type: Dict[str, List[EntityNode]] = {}
        for e in entities:
            t = e.get_entity_type() or "Unknown"
            if t not in by_type:
                by_type[t] = []
            by_type[t].append(e)
        
        for entity_type, type_entities in by_type.items():
            lines.append(f"\n### {entity_type} ({len(type_entities)} entities)")
            display_count = self.ENTITIES_PER_TYPE_DISPLAY
            summary_len = self.ENTITY_SUMMARY_LENGTH
            for e in type_entities[:display_count]:
                summary_preview = (e.summary[:summary_len] + "...") if len(e.summary) > summary_len else e.summary
                lines.append(f"- {e.name}: {summary_preview}")
            if len(type_entities) > display_count:
                lines.append(f"  ... and {len(type_entities) - display_count} more")
        
        return "\n".join(lines)
    
    def _call_llm_with_retry(self, prompt: str, system_prompt: str) -> Dict[str, Any]:
        """Invoke LLM with retry and JSON repair heuristics."""
        import re
        import time
        
        max_attempts = 3
        last_error = None
        
        for attempt in range(max_attempts):
            try:
                response = create_chat_completion(
                    self.client,
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.7 - (attempt * 0.1),
                )
                
                content = extract_chat_completion_text(response)
                finish_reason = response.choices[0].finish_reason
                
                if finish_reason == 'length':
                    logger.warning(f"LLM output truncated (attempt {attempt+1})")
                    content = self._fix_truncated_json(content)
                
                try:
                    return json.loads(content)
                except json.JSONDecodeError as e:
                    logger.warning(f"JSON decode failed (attempt {attempt+1}): {str(e)[:80]}")
                    
                    fixed = self._try_fix_config_json(content)
                    if fixed:
                        return fixed
                    
                    last_error = e
                    
            except Exception as e:
                logger.warning(f"LLM invocation failed (attempt {attempt+1}): {str(e)[:80]}")
                last_error = e
                time.sleep(2 * (attempt + 1))
        
        raise last_error or Exception("LLM call failed")
    
    def _fix_truncated_json(self, content: str) -> str:
        """Attempt to balance truncated JSON braces."""
        content = content.strip()
        
        open_braces = content.count('{') - content.count('}')
        open_brackets = content.count('[') - content.count(']')
        
        if content and content[-1] not in '",}]':
            content += '"'
        
        content += ']' * max(0, open_brackets)
        content += '}' * max(0, open_braces)
        
        return content
    
    def _try_fix_config_json(self, content: str) -> Optional[Dict[str, Any]]:
        """Attempt to repair broken JSON structure."""
        import re
        
        content = self._fix_truncated_json(content)
        json_match = re.search(r'\{[\s\S]*\}', content)
        if json_match:
            json_str = json_match.group()
            
            def fix_string(match):
                s = match.group(0)
                s = s.replace('\n', ' ').replace('\r', ' ')
                s = re.sub(r'\s+', ' ', s)
                return s
            
            json_str = re.sub(r'"[^"\\]*(?:\\.[^"\\]*)*"', fix_string, json_str)
            
            try:
                return json.loads(json_str)
            except Exception:
                try:
                    json_str = re.sub(r'[\x00-\x1f\x7f-\x9f]', ' ', json_str)
                    json_str = re.sub(r'\s+', ' ', json_str)
                    return json.loads(json_str)
                except Exception:
                    pass
        
        return None
    
    def _generate_time_config(self, context: str, num_entities: int) -> Dict[str, Any]:
        """Generate time simulation configuration."""
        context_truncated = context[:self.TIME_CONFIG_CONTEXT_LENGTH]
        max_agents_allowed = max(1, int(num_entities * 0.9))
        
        prompt = f"""Based on the simulation scenario below, generate the time simulation configuration.

{context_truncated}

## Mission
Generate a valid JSON object specifying the time parameters.

### Diurnal Principles:
- Infer the target audience's time zone and behavioral routines from the context.
- Dead hours (midnight to dawn 0-5): minimal activity (~0.05 multiplier).
- Morning hours (6-8): gradual awakening (~0.4 multiplier).
- Working hours (9-18): moderate steady activity (~0.7 multiplier).
- Evening peak hours (19-22): primary active period (~1.5 multiplier).
- Late evening (23): winding down (~0.5 multiplier).
- Adjust hours flexibly according to stakeholder profiles (e.g. students active later, institutional accounts active during business hours).

### Output JSON Format (no markdown code blocks):
{{
    "total_simulation_hours": 72,
    "minutes_per_round": 60,
    "agents_per_hour_min": 5,
    "agents_per_hour_max": 50,
    "peak_hours": [19, 20, 21, 22],
    "off_peak_hours": [0, 1, 2, 3, 4, 5],
    "morning_hours": [6, 7, 8],
    "work_hours": [9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
    "reasoning": "Brief explanation of the rationale for this schedule"
}}

Field Definitions:
- total_simulation_hours (int): Total simulation duration (24-168 hours).
- minutes_per_round (int): Duration per simulation round in minutes (30-120, default 60).
- agents_per_hour_min (int): Minimum activated agents per hour (range: 1-{max_agents_allowed}).
- agents_per_hour_max (int): Maximum activated agents per hour (range: 1-{max_agents_allowed}).
- peak_hours (int array): Evening peak activity hours.
- off_peak_hours (int array): Low activity hours.
- morning_hours (int array): Morning hours.
- work_hours (int array): Working business hours.
- reasoning (string): Brief rationale."""

        system_prompt = "You are a social media simulation specialist. Return pure JSON without extra markdown. Ensure the time configuration respects realistic diurnal patterns."
        system_prompt = f"{system_prompt}\n\n{get_language_instruction()}"

        try:
            return self._call_llm_with_retry(prompt, system_prompt)
        except Exception as e:
            logger.warning(f"Time config LLM generation failed: {e}, falling back to defaults")
            return self._get_default_time_config(num_entities)
    
    def _get_default_time_config(self, num_entities: int) -> Dict[str, Any]:
        """Return standard default diurnal time configuration."""
        return {
            "total_simulation_hours": 72,
            "minutes_per_round": 60,
            "agents_per_hour_min": max(1, num_entities // 15),
            "agents_per_hour_max": max(5, num_entities // 5),
            "peak_hours": [19, 20, 21, 22],
            "off_peak_hours": [0, 1, 2, 3, 4, 5],
            "morning_hours": [6, 7, 8],
            "work_hours": [9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
            "reasoning": "Using default diurnal schedule configuration (1 hour per round)"
        }
    
    def _parse_time_config(self, result: Dict[str, Any], num_entities: int) -> TimeSimulationConfig:
        """Parse time configuration result and validate bounds."""
        agents_per_hour_min = result.get("agents_per_hour_min", max(1, num_entities // 15))
        agents_per_hour_max = result.get("agents_per_hour_max", max(5, num_entities // 5))
        
        if agents_per_hour_min > num_entities:
            logger.warning(f"agents_per_hour_min ({agents_per_hour_min}) exceeds total agents ({num_entities}), adjusting")
            agents_per_hour_min = max(1, num_entities // 10)
        
        if agents_per_hour_max > num_entities:
            logger.warning(f"agents_per_hour_max ({agents_per_hour_max}) exceeds total agents ({num_entities}), adjusting")
            agents_per_hour_max = max(agents_per_hour_min + 1, num_entities // 2)
        
        if agents_per_hour_min >= agents_per_hour_max:
            agents_per_hour_min = max(1, agents_per_hour_max // 2)
            logger.warning(f"agents_per_hour_min >= max, adjusted to {agents_per_hour_min}")
        
        return TimeSimulationConfig(
            total_simulation_hours=result.get("total_simulation_hours", 72),
            minutes_per_round=result.get("minutes_per_round", 60),
            agents_per_hour_min=agents_per_hour_min,
            agents_per_hour_max=agents_per_hour_max,
            peak_hours=result.get("peak_hours", [19, 20, 21, 22]),
            off_peak_hours=result.get("off_peak_hours", [0, 1, 2, 3, 4, 5]),
            off_peak_activity_multiplier=0.05,
            morning_hours=result.get("morning_hours", [6, 7, 8]),
            morning_activity_multiplier=0.4,
            work_hours=result.get("work_hours", list(range(9, 19))),
            work_activity_multiplier=0.7,
            peak_activity_multiplier=1.5
        )
    
    def _generate_event_config(
        self, 
        context: str, 
        simulation_requirement: str,
        entities: List[EntityNode]
    ) -> Dict[str, Any]:
        """Generate event configuration and initial posts."""
        entity_types_available = list(set(
            e.get_entity_type() or "Unknown" for e in entities
        ))
        
        type_examples = {}
        for e in entities:
            etype = e.get_entity_type() or "Unknown"
            if etype not in type_examples:
                type_examples[etype] = []
            if len(type_examples[etype]) < 3:
                type_examples[etype].append(e.name)
        
        type_info = "\n".join([
            f"- {t}: {', '.join(examples)}" 
            for t, examples in type_examples.items()
        ])
        
        context_truncated = context[:self.EVENT_CONFIG_CONTEXT_LENGTH]
        
        prompt = f"""Based on the simulation scenario below, generate the event configuration.

Simulation Requirements: {simulation_requirement}

{context_truncated}

## Available Entity Types and Representatives
{type_info}

## Mission
Generate a valid JSON object specifying the event parameters:
- Extract key trending topic keywords
- Describe narrative progression direction
- Design initial trigger posts, where **each post must specify poster_type**

**IMPORTANT**: poster_type must be selected from the available entity types above, so each post can be assigned to a matching agent.
Example: Official statements from Official/University, news bulletins from MediaOutlet, student perspectives from Student.

Output JSON Format (no markdown):
{{
    "hot_topics": ["keyword1", "keyword2"],
    "narrative_direction": "<description of narrative trajectory>",
    "initial_posts": [
        {{"content": "Post content text", "poster_type": "ExactEntityType"}},
        ...
    ],
    "reasoning": "<brief explanation>"
}}"""

        system_prompt = "You are a public discourse intelligence analyst. Return pure JSON. Ensure poster_type matches the available entity types exactly."
        system_prompt = f"{system_prompt}\n\n{get_language_instruction()}\nIMPORTANT: The 'poster_type' field value MUST be in English PascalCase exactly matching the available entity types. Only 'content', 'narrative_direction', 'hot_topics' and 'reasoning' fields should use the specified language."

        try:
            return self._call_llm_with_retry(prompt, system_prompt)
        except Exception as e:
            logger.warning(f"Event config LLM generation failed: {e}, falling back to defaults")
            return {
                "hot_topics": [],
                "narrative_direction": "",
                "initial_posts": [],
                "reasoning": "Using default configuration"
            }
    
    def _parse_event_config(self, result: Dict[str, Any]) -> EventConfig:
        """Parse event configuration result."""
        return EventConfig(
            initial_posts=result.get("initial_posts", []),
            scheduled_events=[],
            hot_topics=result.get("hot_topics", []),
            narrative_direction=result.get("narrative_direction", "")
        )
    
    def _assign_initial_post_agents(
        self,
        event_config: EventConfig,
        agent_configs: List[AgentActivityConfig]
    ) -> EventConfig:
        """Assign appropriate author agents to initial trigger posts."""
        if not event_config.initial_posts:
            return event_config
        
        agents_by_type: Dict[str, List[AgentActivityConfig]] = {}
        for agent in agent_configs:
            atype = agent.entity_type
            if atype not in agents_by_type:
                agents_by_type[atype] = []
            agents_by_type[atype].append(agent)
        
        assigned_agents = set()
        
        for post in event_config.initial_posts:
            target_type = post.get("poster_type", "")
            assigned_id = None
            
            matching_agents = agents_by_type.get(target_type, [])
            for agent in matching_agents:
                if agent.agent_id not in assigned_agents:
                    assigned_id = agent.agent_id
                    assigned_agents.add(assigned_id)
                    break
            
            if assigned_id is None and matching_agents:
                assigned_id = matching_agents[0].agent_id
            
            if assigned_id is None and agent_configs:
                for agent in agent_configs:
                    if agent.agent_id not in assigned_agents:
                        assigned_id = agent.agent_id
                        assigned_agents.add(assigned_id)
                        break
                if assigned_id is None:
                    assigned_id = agent_configs[0].agent_id
            
            post["poster_agent_id"] = assigned_id
            if assigned_id is not None:
                agent = next((a for a in agent_configs if a.agent_id == assigned_id), None)
                if agent:
                    post["poster_name"] = agent.entity_name
                    post["poster_entity_type"] = agent.entity_type
        
        return event_config
    
    def _generate_agent_configs_batch(
        self,
        context: str,
        entities: List[EntityNode],
        start_idx: int,
        simulation_requirement: str
    ) -> List[AgentActivityConfig]:
        """Generate activity configurations for a batch of agents."""
        entity_list = []
        summary_len = self.AGENT_SUMMARY_LENGTH
        for i, e in enumerate(entities):
            entity_list.append({
                "agent_id": start_idx + i,
                "entity_name": e.name,
                "entity_type": e.get_entity_type() or "Unknown",
                "summary": e.summary[:summary_len] if e.summary else ""
            })
        
        prompt = f"""Based on the information below, generate social media activity configurations for each entity.

Simulation Requirements: {simulation_requirement}

## Entity List
```json
{json.dumps(entity_list, ensure_ascii=False, indent=2)}
```

## Mission
Generate activity configurations for each entity adhering to these principles:
- Align active hours with the target stakeholder daily routines.
- Official entities (University/GovernmentAgency): low activity (0.1-0.3), business hours (9-17), deliberate response (60-240 mins), high influence (2.5-3.0).
- Media (MediaOutlet): moderate activity (0.4-0.6), broad hours (8-23), rapid response (5-30 mins), high influence (2.0-2.5).
- Individuals (Student/Person/Alumni): higher activity (0.6-0.9), evening hours (18-23), fast response (1-15 mins), normal influence (0.8-1.2).
- Experts / Public Figures: moderate activity (0.4-0.6), elevated influence (1.5-2.0).

Return JSON format:
{{
    "agent_configs": [
        {{
            "agent_id": <matching input id>,
            "activity_level": <0.0-1.0>,
            "posts_per_hour": <float>,
            "comments_per_hour": <float>,
            "active_hours": [<array of active hours 0-23>],
            "response_delay_min": <int>,
            "response_delay_max": <int>,
            "sentiment_bias": <-1.0 to 1.0>,
            "stance": "<supportive/opposing/neutral/observer>",
            "influence_weight": <float>
        }}
    ]
}}"""

        system_prompt = "You are a behavioral simulation analyst. Return pure JSON conforming to realistic social dynamics."
        system_prompt = f"{system_prompt}\n\n{get_language_instruction()}\nIMPORTANT: The 'stance' field value MUST be one of the English strings: 'supportive', 'opposing', 'neutral', 'observer'. All JSON field names and numeric values must remain unchanged. Only natural language text fields should use the specified language."

        try:
            result = self._call_llm_with_retry(prompt, system_prompt)
            llm_configs = {cfg["agent_id"]: cfg for cfg in result.get("agent_configs", [])}
        except Exception as e:
            logger.warning(f"Agent config batch LLM generation failed: {e}, using heuristic fallbacks")
            llm_configs = {}
        
        configs = []
        for i, entity in enumerate(entities):
            agent_id = start_idx + i
            cfg = llm_configs.get(agent_id, {})
            
            if not cfg:
                cfg = self._generate_agent_config_by_rule(entity)
            
            config = AgentActivityConfig(
                agent_id=agent_id,
                entity_uuid=entity.uuid,
                entity_name=entity.name,
                entity_type=entity.get_entity_type() or "Unknown",
                activity_level=cfg.get("activity_level", 0.5),
                posts_per_hour=cfg.get("posts_per_hour", 0.5),
                comments_per_hour=cfg.get("comments_per_hour", 1.0),
                active_hours=cfg.get("active_hours", list(range(9, 23))),
                response_delay_min=cfg.get("response_delay_min", 5),
                response_delay_max=cfg.get("response_delay_max", 60),
                sentiment_bias=cfg.get("sentiment_bias", 0.0),
                stance=cfg.get("stance", "neutral"),
                influence_weight=cfg.get("influence_weight", 1.0)
            )
            configs.append(config)
        
        return configs
    
    def _generate_agent_config_by_rule(self, entity: EntityNode) -> Dict[str, Any]:
        """Heuristic rule-based fallback configuration for an individual agent."""
        entity_type = (entity.get_entity_type() or "Unknown").lower()
        
        if entity_type in ["university", "governmentagency", "ngo"]:
            return {
                "activity_level": 0.2,
                "posts_per_hour": 0.1,
                "comments_per_hour": 0.05,
                "active_hours": list(range(9, 18)),
                "response_delay_min": 60,
                "response_delay_max": 240,
                "sentiment_bias": 0.0,
                "stance": "neutral",
                "influence_weight": 3.0
            }
        elif entity_type in ["mediaoutlet"]:
            return {
                "activity_level": 0.5,
                "posts_per_hour": 0.8,
                "comments_per_hour": 0.3,
                "active_hours": list(range(7, 24)),
                "response_delay_min": 5,
                "response_delay_max": 30,
                "sentiment_bias": 0.0,
                "stance": "observer",
                "influence_weight": 2.5
            }
        elif entity_type in ["professor", "expert", "official"]:
            return {
                "activity_level": 0.4,
                "posts_per_hour": 0.3,
                "comments_per_hour": 0.5,
                "active_hours": list(range(8, 22)),
                "response_delay_min": 15,
                "response_delay_max": 90,
                "sentiment_bias": 0.0,
                "stance": "neutral",
                "influence_weight": 2.0
            }
        elif entity_type in ["student"]:
            return {
                "activity_level": 0.8,
                "posts_per_hour": 0.6,
                "comments_per_hour": 1.5,
                "active_hours": [8, 9, 10, 11, 12, 13, 18, 19, 20, 21, 22, 23],
                "response_delay_min": 1,
                "response_delay_max": 15,
                "sentiment_bias": 0.0,
                "stance": "neutral",
                "influence_weight": 0.8
            }
        elif entity_type in ["alumni"]:
            return {
                "activity_level": 0.6,
                "posts_per_hour": 0.4,
                "comments_per_hour": 0.8,
                "active_hours": [12, 13, 19, 20, 21, 22, 23],
                "response_delay_min": 5,
                "response_delay_max": 30,
                "sentiment_bias": 0.0,
                "stance": "neutral",
                "influence_weight": 1.0
            }
        else:
            return {
                "activity_level": 0.7,
                "posts_per_hour": 0.5,
                "comments_per_hour": 1.2,
                "active_hours": [9, 10, 11, 12, 13, 18, 19, 20, 21, 22, 23],
                "response_delay_min": 2,
                "response_delay_max": 20,
                "sentiment_bias": 0.0,
                "stance": "neutral",
                "influence_weight": 1.0
            }
