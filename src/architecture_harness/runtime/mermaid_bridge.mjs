import { JSDOM } from "jsdom";

const input = JSON.parse(await new Promise((resolve) => {
  let data = "";
  process.stdin.setEncoding("utf8");
  process.stdin.on("data", (chunk) => { data += chunk; });
  process.stdin.on("end", () => resolve(data));
}));

const dom = new JSDOM("<!doctype html><html><body></body></html>");
globalThis.window = dom.window;
globalThis.document = dom.window.document;
globalThis.Element = dom.window.Element;

const { default: mermaid } = await import("mermaid");
mermaid.initialize({ startOnLoad: false, securityLevel: "strict" });

const parsed = await mermaid.parse(input.text);
const diagram = await mermaid.mermaidAPI.getDiagramFromText(input.text);
const db = diagram.db;
const nodes = new Map();
const edges = [];
const subgraphs = {};

const addNode = (id, label = id) => {
  if (id !== undefined && id !== null && String(id)) {
    const key = String(id);
    if (!nodes.has(key) || String(label ?? id) !== key) nodes.set(key, String(label ?? id));
  }
};
const addEdge = (source, target, label = "") => {
  if (source !== undefined && target !== undefined) {
    addNode(source);
    addNode(target);
    edges.push({ source: String(source), target: String(target), label: String(label ?? "") });
  }
};
const values = (value) => value instanceof Map ? [...value.values()] : Array.isArray(value) ? value : [];

if (db.vertices && db.edges) {
  for (const vertex of values(db.vertices)) addNode(vertex.id, vertex.text ?? vertex.label ?? vertex.id);
  for (const edge of db.edges) addEdge(edge.start, edge.end, edge.text);
  for (const group of db.subGraphs ?? []) {
    const id = String(group.id ?? group.title ?? "subgraph");
    subgraphs[id] = (group.nodes ?? []).map(String);
  }
} else if (db.relations && db.classes) {
  for (const klass of values(db.classes)) addNode(klass.id, klass.label ?? klass.text ?? klass.id);
  for (const relation of db.relations) addEdge(relation.id1, relation.id2, relation.title ?? "");
} else if (db.state?.records) {
  for (const actor of values(db.state.records.actors)) addNode(actor.name, actor.description ?? actor.name);
  for (const message of db.state.records.messages ?? []) addEdge(message.from, message.to, message.message);
} else if (db.entities && db.relationships) {
  const entityIds = new Map();
  for (const [name, entity] of db.entities.entries()) {
    addNode(name, entity.label ?? name);
    entityIds.set(entity.id, name);
  }
  for (const relation of db.relationships) {
    addEdge(entityIds.get(relation.entityA) ?? relation.entityA, entityIds.get(relation.entityB) ?? relation.entityB, relation.roleA);
  }
} else if (db.nodes && db.edges) {
  for (const node of values(db.nodes)) addNode(node.id, node.label ?? node.title ?? node.id);
  for (const edge of db.edges) addEdge(edge.start ?? edge.lhsId, edge.end ?? edge.rhsId, edge.label ?? edge.title);
}

// The official Langium AST currently covers Mermaid's newly migrated diagram families,
// including architecture-beta. Use it when the legacy diagram DB has no common graph view.
if (nodes.size === 0 && parsed.diagramType === "architecture") {
  const { parse } = await import("@mermaid-js/parser");
  const ast = await parse("architecture", input.text);
  for (const service of ast.services ?? []) addNode(service.id, service.title ?? service.id);
  for (const junction of ast.junctions ?? []) addNode(junction.id, junction.id);
  for (const edge of ast.edges ?? []) addEdge(edge.lhsId, edge.rhsId);
  for (const group of ast.groups ?? []) subgraphs[String(group.id)] = [];
  for (const service of ast.services ?? []) {
    const groupId = service.in?.$refText ?? service.in?.ref?.id;
    if (groupId && subgraphs[groupId]) subgraphs[groupId].push(String(service.id));
  }
}

process.stdout.write(JSON.stringify({
  diagram_type: parsed.diagramType,
  nodes: [...nodes].map(([id, label]) => ({ id, label })),
  edges,
  subgraphs,
  source: input.source,
}));
