# Our hybrid RAG approach

Use a hybrid pre-graph RAG approach where each chunk/entity has consistent metadata parameters (like "type" and "topic") that enable querying for related entities without the overhead of a full graph solution.

## Practical Technique: Parametric Enrichment

- **Parameterized chunks/rows:** When storing each chunk or entity, you can add consistent extra fields for each row:
  - “type”: Defines what kind of entity (person, place, organization, concept, etc.) is represented.
  - "topic". 
- **Multi-row entities:** An entity with multiple senses or roles can have several rows, each representing a different context or meaning, with unique parameter values for each.

### How Querying Works

- **Filtered retrieval:** During semantic search (vector similarity), you can filter, group, or boost results based on these extra parameters, allowing the system to:
  - Prioritize noun senses for a “who” question.
  - Filter out irrelevant entity-types.
  - Surface related attributes (e.g., “find related companies,” “list connected verbs”).
- **Soft-linking:** This technique allows easy retrieval of related entities or concepts with matching parameters—mimicking “edges” in a lightweight manner, without a true graph traversal. For example, all “person” type rows connected by “collaborated-with” verb parameters can be grouped or filtered for output.

## Example

Chunk/Entity: "Apple fruit", embedding: [0.41, ...], type: Food, topic: Nutrition
Chunk/Entity: "Apple company", embedding: [0.92, ...], type: Organization, topic: Tech
Chunk/Entity: "run", embedding: [0.61, ...], type: Action, topic: Fitness

A query for tech organizations can filter for `type="Organization"` and `topic="Tech"`, retrieving “Apple company” without needing to use graph traversal.

This approach—sometimes called “semantic chunking” or “metadata enrichment”—lets you capture many benefits of graph-style linking, while keeping your system lightweight and easy to manage.
