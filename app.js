
"use strict";
const S=window.LIFE_CODE_SNAPSHOT;if(!S)throw new Error("LIFE-CODE snapshot did not load.");
const P=window.LIFE_CODE_PROGRAM_CONTEXT||{benchmarks:[],prediction_maturity_ladder:[],program_history:[],sources:[]};
const F=window.LIFE_CODE_FRAMEWORK_CONTEXT||{};
const $=id=>document.getElementById(id),objects=S.code_objects||[],byId=Object.fromEntries(objects.map(x=>[x.object_id,x]));
const artById=Object.fromEntries((S.artifacts||[]).map(x=>[x.artifact_id,x])),expById=Object.fromEntries((S.experiments||[]).map(x=>[x.experiment_id,x]));
let savedLens;try{savedLens=localStorage.getItem("lifecode-lens")}catch{}
let lens=["explore","learn","research"].includes(savedLens)?savedLens:"explore",view="home",current=null,tab="overview";

const GLOSSARY={
 DNA:"The molecule that stores hereditary information using four chemical bases usually written A, C, G and T.",
 genome:"The complete DNA sequence being studied for an organism or cell.",
 "exact match":"The same sequence of A, C, G and T appears without substitutions in both places being compared.",
 "k-mer":"A DNA word exactly k bases long. For example, a 16-mer contains 16 DNA letters.",
 "annotation-blind":"The search is performed without using gene names or known biological labels to guide where to look.",
 calibration:"A test used to learn how a method behaves and where its limits are before making broader claims.",
 "null model":"A comparison model representing what we might expect from chance under specified constraints.",
 "held-out test":"Data deliberately excluded while a rule is formed, then used afterward to test whether the rule transfers.",
 module:"A higher-level grouping or relationship among lower-level sequence objects.",
 provenance:"The traceable path back from a displayed result to its source record or artifact.",
 freeze:"The point where a discovery result is locked before biological labels are revealed.",
 "post-freeze annotation":"Biological interpretation added only after the sequence result has already been frozen.",
 falsified:"A tested model that failed its stated test. It stays in the Codebook as useful negative evidence.",
 block:"An exact released DNA sequence object.",
 "evidence tier":"A project label describing what evidence is allowed to appear in a given release layer."
,
 "Codebook":"LIFE-CODE's structured evidence store: sequence objects, relationships, experiments, measurements, annotations, claims, provenance and negative results.",
 "history edge":"A typed, evidence-bounded hypothesis about how a biological object changed or moved through evolutionary history.",
 "stratum":"The evolutionary breadth or depth over which a structure is observed to persist.",
 "reachability":"Whether a candidate biological state is compatible with the evidence and constraints available to the system.",
 "resilience":"The ability of a biological system to tolerate, repair, compensate for, or route around failure.",
 "retrodiction":"Predicting a real state that is deliberately hidden until after the prediction has been frozen.",
 "evidence state":"A label separating what was observed, experimentally produced, interpreted, speculated, or falsified.",
 "visual truth state":"A label describing whether a displayed state is observed, reconstructed, retrodicted, interpolated, extrapolated, counterfactual, or unsupported."};
const plain={
"PC1-BLOCK-B24":"The 24-letter block B contains the shared 16-letter core in the bacterium and archaeon.",
"PC1-CORE-16":"A 16-letter core inside that block also appears in yeast.",
"PC1-BLOCK-A25":"The 25-letter block A appears before block B in the six recorded neighborhoods.",
"PC1-MODULE-RIBO":"Those pieces form a repeated neighborhood. Only after the blind result was frozen did biological annotation connect it to ribosomal organization.",
"PC2-BLOCK-C25":"One of two exact DNA pieces recovered independently in E. coli and yeast.",
"PC2-BLOCK-D17":"The second exact piece in the same blind comparison.",
"PC2-MODULE-FBA":"The two pieces landed at matching relative positions in both genomes. After freezing the result, both were found inside fructose-bisphosphate aldolase genes.",
"NEG-FLAT-DICT":"A simple 'one big dictionary of exact DNA words' model did not compress the tested genomes better than raw 2-bit DNA after costs.",
"NEG-EXACT-GAP":"A rule requiring the exact same distance between two DNA pieces did not transfer to the held-out third domain.",
"NEG-ORDER-WINDOW":"A looser rule—A before B within 10,000 bases—also failed to transfer to the held-out third domain."
};
const notProof={
"PC1-MODULE-RIBO":"This does not reconstruct the whole evolutionary history of ribosomes or mitochondria.",
"PC2-MODULE-FBA":"This validates the blind-recovery method on this case; it does not prove a universal genomic language.",
"NEG-FLAT-DICT":"The failure of one simple model does not mean genomes lack reusable structure.",
"NEG-EXACT-GAP":"The failure of exact spacing does not rule out more flexible relationships.",
"NEG-ORDER-WINDOW":"The failure of this window rule does not mean function itself is unconserved."
};

function esc(v){return String(v??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[c]))}
function fmt(v){return v===null||v===undefined||v===""?"—":esc(v)}
function comma(v){return Number(v).toLocaleString("en-US")}
function measures(subject,metric){return (S.measurements||[]).filter(m=>m.subject_id===subject&&(!metric||m.metric===metric))}
function mval(subject,metric,notes){const a=measures(subject,metric).find(m=>!notes||(m.notes||"").includes(notes));return a?a.value_num??a.value_text:null}
function setExplorer(on){$("explorerPane").hidden=!on;$("workspace").classList.toggle("has-explorer",!!on)}
function badge(s,c=""){return `<span class="badge ${c}">${esc(s)}</span>`}
function term(t,label=t){return `<button class="termchip" data-term="${esc(t)}">${esc(label)}</button>`}
function keyValue(rows){return `<table><tr><th>Field</th><th>Value</th></tr>${rows.map(([k,v])=>`<tr><td>${esc(k)}</td><td>${fmt(v)}</td></tr>`).join("")}</table>`}
function setLens(x){
 lens=x;tab="overview";try{localStorage.setItem("lifecode-lens",x)}catch{};
 document.body.classList.remove("lens-learn","lens-research");if(x==="learn")document.body.classList.add("lens-learn");if(x==="research")document.body.classList.add("lens-research");
 [["exploreLens","explore"],["learnLens","learn"],["researchLens","research"]].forEach(([id,val])=>{$(id).classList.toggle("active",x===val);$(id).setAttribute("aria-pressed",x===val)});
 render();
}
function setView(v){
 window.history.replaceState(null,"",location.pathname+location.search);view=v;current=null;tab="overview";document.querySelectorAll(".nav").forEach(b=>b.classList.toggle("active",b.dataset.view===v));
 setExplorer(v==="codebook");renderList();render();$("content").focus({preventScroll:true});
}
function bindTerms(){
 document.querySelectorAll("[data-term]").forEach(b=>b.onclick=()=>{const t=b.dataset.term;alert(`${t}\n\n${GLOSSARY[t]||"Definition not available."}`)});
 document.querySelectorAll("[data-route]").forEach(b=>b.onclick=()=>setView(b.dataset.route));
}
function home(){
 $("content").innerHTML=`
 <div class=hero><div class=eyebrow>What is LIFE-CODE?</div>
 <h2>We are testing whether genomes contain reusable sequence pieces and relationships that can be discovered before we use biological labels.</h2>
 <p class=answer>In plain terms: can a computer find recurring DNA structure first, lock what it found, and only afterward ask biology what those pieces are?</p></div>
 <div class=stepbar>
  <div class=step><b>1 · Ignore the labels</b>Search raw DNA without starting from gene names.</div>
  <div class=step><b>2 · Find recurrence</b>Record exact pieces and relationships that repeat.</div>
  <div class=step><b>3 · Freeze the result</b>Lock the sequence result before interpretation.</div>
  <div class=step><b>4 · Reveal meaning</b>Only then compare the result with known biology.</div>
 </div>
 <div class="grid">
  <div class=metric><div class=n>${S.counts.code_objects}</div><div class=l>released Codebook objects</div></div>
  <div class=metric><div class=n>${S.counts.experiments}</div><div class=l>released proof/calibration experiments</div></div>
  <div class=metric><div class=n>${S.counts.measurements}</div><div class=l>released measurements</div></div>
 </div>
 <div class=card><h3>Recovered evidence is now explorable</h3><p>${S.vocabulary.length} exact shared sequences, ${S.occurrences.length} verified focused locations, and an auditable correction trail now connect the original calibration to this Codebook.</p><button class=action data-route="recovery">Explore the recovered evidence →</button></div><div class="card plainOnly"><div class=question>Why would anyone care?</div><p>If useful structure can be recovered without telling the system what genes are supposed to matter, the Codebook can become a neutral map of recurring genomic structure rather than a list built from existing annotations.</p></div>
 <div class="card learnBlock"><h3>What makes this different from simply finding matching DNA?</h3><p>Matching sequence is old science. LIFE-CODE is testing a stricter architecture: annotation-blind discovery, explicit physical relationships, frozen results, post-freeze interpretation, negative calibrations, provenance, and held-out tests. The contribution—if it survives larger experiments—is the combined method, not the existence of ${term("k-mer","k-mers")} or conservation.</p></div>
 <div class="card researchBlock"><h3>Release state</h3>${keyValue([["Snapshot schema",S.snapshot_schema],["Generated UTC",S.generated_utc],["Source database",S.source_database.filename],["Source DB SHA-256",S.source_database.sha256],["Release gate",S.public_release_gates.passed?"PASS":"FAIL"]])}</div>
 <div class=card><div class=question>Four questions, one evidence system</div><h3>LIFE-CODE is bigger than a DNA-word search.</h3><p>The released Codebook is the first layer. The larger framework asks four connected questions:</p><div class=pillargrid>${(F.pillars||[]).map(x=>`<div class=pillar><div class=pid>${esc(x.id)}</div><h3>${esc(x.question)}</h3><p>${esc(x.plain)}</p><button class=action data-route="${esc(x.route)}">Open ${esc(x.id.toLowerCase())} →</button></div>`).join("")}</div></div>
 <div class=callout><b>Important:</b> this is calibration-stage science. LIFE-CODE has not “decoded DNA,” and the current public release does not contain EXP-0002 outcome values.</div>
 <div><button class=action id=goFindings>See what the blind searches actually found →</button></div>`;
 $("goFindings").onclick=()=>setView("findings");bindTerms();
}
function findings(){
 const spacings=measures("PC1-MODULE-RIBO","observed_A_to_B_spacing").map(x=>x.value_num);
 const pc2C=byId["PC2-BLOCK-C25"],pc2D=byId["PC2-BLOCK-D17"];
 $("content").innerHTML=`
 <div class=hero><div class=eyebrow>What we found</div><h2>Start with the result, then decide how deep you want to go.</h2><p>Two proof cases survived their frozen calibration tests. Three intuitive models failed. All five outcomes stay visible.</p></div>
 <div class=storygrid>
  <div class=story><div class=question>Proof Case 0001 · cross-domain structure</div><h3>A repeated DNA neighborhood appeared across very different organisms.</h3>
   <div class=statstrip><div class=stat><b>${comma(mval("PC-0001","shared_16mers"))}</b><span>exact 16-letter words shared by all three pilot domains</span></div><div class=stat><b>${byId["PC1-BLOCK-A25"].length_bp} / ${byId["PC1-BLOCK-B24"].length_bp} / ${byId["PC1-CORE-16"].length_bp}</b><span>base-pair sizes of A, B, and the core inside B</span></div><div class=stat><b>${mval("PC-0001","spacing_range")} bp</b><span>range across six observed A→B spacings</span></div></div>
   <p>Six observed spacings cluster around roughly three thousand bases: <b>${spacings.map(x=>comma(x)).join(", ")} bp</b>.</p>
   <div class="plainOnly callout"><b>Picture it:</b> not just the same short phrase in different books, but another phrase repeatedly appearing nearby.</div>
   <div class=learnBlock><p>A 5,000,000-draw spatial null produced <b>zero</b> random cases matching all five E. coli downstream hits. This is calibration evidence, not a corrected publication p-value.</p></div>
   <div class=researchBlock><div class=compare><div><div class=statusnote>older PC-0001 summary</div><div class=value>${mval("PC-0001","mono_null_mean")} / ${mval("PC-0001","dinuc_null_mean")}</div><span>mono / dinucleotide k=16 null means</span></div><div><div class=statusnote>full vocabulary ladder</div><div class=value>${mval("CAL-VOCAB","mono_null_mean_k16")} / ${mval("CAL-VOCAB","dinuc_null_mean_k16")}</div><span>mono / dinucleotide k=16 null means</span></div></div><div class=callout><b>Open provenance issue:</b> these k=16 null summaries disagree slightly and remain explicitly unresolved until their source lineage is reconciled.</div></div>
   <button class=action data-goto="PC1-MODULE-RIBO">Open Codebook evidence</button>
  </div>
  <div class=story><div class=question>Proof Case 0002 · blind coding structure</div><h3>The search found a matching two-block pattern before it knew the gene names.</h3>
   <div class=statstrip><div class=stat><b>${comma(mval("PC-0002","shared_16mers"))}</b><span>E. coli ↔ yeast shared exact 16-mers</span></div><div class=stat><b>${mval("PC-0002","raw_start_spacing")} bp</b><span>raw start spacing in both genomes</span></div><div class=stat><b>${mval("PC-0002","coding_region_length_each")} bp</b><span>length of each coding region</span></div></div>
   <p>Six high-complexity multiblock clusters were recovered; five were mitochondrial. The remaining non-mitochondrial module became the FBA proof case after post-freeze annotation.</p>
   <div class=learnBlock><div class=simpletable><div class=simpleRow><b>Block C</b><span><code>${esc(pc2C?.sequence||"sequence in Codebook")}</code></span></div><div class=simpleRow><b>Block D</b><span><code>${esc(pc2D?.sequence||"sequence in Codebook")}</code></span></div><div class=simpleRow><b>Nucleotide identity</b><span>${mval("PC-0002","positionwise_nucleotide_identity")}% across the 1080-bp coding regions</span></div><div class=simpleRow><b>Protein identity</b><span>${mval("PC-0002","protein_identity_corresponding_positions")}% at corresponding translated positions</span></div></div></div>
   <div class=researchBlock><p>Block coding starts: C=${mval("PC-0002","block_C_coding_start_0based")}, D=${mval("PC-0002","block_D_coding_start_0based")} (0-based). Post-freeze annotation identified <i>E. coli</i> <code>fbaA</code> and yeast <code>FBA1</code>.</p></div>
   <button class=action data-goto="PC2-MODULE-FBA">Open Codebook evidence</button>
  </div>
 </div>
 <div class=finding><div class=question>And the failures?</div><h3>Three simple models were tested hard enough to fail.</h3><p class=why>They are not footnotes. They tell us that reusable structure—if it exists at larger scale—is not captured by a flat exact dictionary, an exact fixed gap, or a simple “A before B within 10 kb” rule.</p><button class=action id=goModels>See what failed and the actual test counts →</button></div>`;
 document.querySelectorAll("[data-goto]").forEach(b=>b.onclick=()=>selectObject(b.dataset.goto));$("goModels").onclick=()=>setView("models");
}
function initFilters(){
 const types=[...new Set(objects.map(o=>o.object_type))].sort(),states=[...new Set(objects.map(o=>o.evidence_state))].sort();
 $("type").innerHTML='<option value="">All</option>'+types.map(x=>`<option>${esc(x)}</option>`).join("");
 $("state").innerHTML='<option value="">All</option>'+states.map(x=>`<option>${esc(x)}</option>`).join("");
}
function filtered(){const q=$("search").value.trim().toLowerCase(),t=$("type").value,s=$("state").value;return objects.filter(o=>(!q||[o.object_id,o.object_type,o.label,o.description,o.status,o.sequence,...(S.object_aliases||[]).filter(a=>a.canonical_object_id===o.object_id).map(a=>a.legacy_object_id)].join(" ").toLowerCase().includes(q))&&(!t||o.object_type===t)&&(!s||o.evidence_state===s))}
function renderList(){
 const f=filtered();$("count").textContent=`${f.length} of ${objects.length} objects`;
 $("objectList").innerHTML=f.map(o=>`<button class="item ${current===o.object_id?"active":""}" data-object="${esc(o.object_id)}"><div class=itemid>${esc(o.object_id)}</div><div class=itemmeta>${esc(o.object_type)} · ${esc(o.evidence_state)}</div><div class=itemlabel>${esc(o.label)}</div></button>`).join("");
 document.querySelectorAll("[data-object]").forEach(b=>b.onclick=()=>{current=b.dataset.object;tab="overview";renderList();renderObject()});
}
function selectObject(id){id=resolveObjectId(id);window.history.replaceState(null,"","#object="+encodeURIComponent(id));view="codebook";current=id;tab="overview";document.querySelectorAll(".nav").forEach(b=>b.classList.toggle("active",b.dataset.view==="codebook"));setExplorer(true);renderList();renderObject()}
function objectLanding(){
 $("content").innerHTML=`<div class=hero><div class=eyebrow>Explore the Codebook</div><h2>Choose a released object. Start with the explanation, then open as much evidence as you want.</h2><p>The reading-depth control changes presentation, not the underlying record.</p></div><div class=card><h3>What kinds of objects are here?</h3><p><b>Blocks</b> are exact DNA sequences. <b>Modules</b> are relationships among pieces. <b>Falsified models</b> are tested ideas that failed.</p></div>`;
}
function objectTabs(){let n=lens==="explore"?["overview","connections","locations"]:lens==="learn"?["overview","connections","locations","evidence"]:["overview","graph","locations","measurements","provenance","raw"];return `<div class=tabs>${n.map(x=>`<button class="tab ${tab===x?"active":""}" data-tab="${x}">${x}</button>`).join("")}</div>`}
function renderObject(){
 const o=byId[current];if(!o){objectLanding();return}const anns=S.annotations.filter(a=>a.subject_type==="OBJECT"&&a.subject_id===o.object_id),ex=expById[o.discovery_experiment_id],art=artById[o.source_artifact_id];
 let html=objectTabs();
 if(tab==="overview"){
  html+=`<div class=card><div class=badges>${badge(o.object_type)}${badge(o.evidence_state,o.evidence_state==="FALSIFIED"?"bad":"good")}${badge("TIER "+o.evidence_tier)}</div><h2>${esc(o.label)}</h2>
  <p class=answer>${esc(plain[o.object_id]||o.description||"Released Codebook object.")}</p>
  ${notProof[o.object_id]?`<div class=callout><b>What this does not prove:</b> ${esc(notProof[o.object_id])}</div>`:""}
  <div class=learnBlock><h3>Scientific description</h3><p>${fmt(o.description)}</p></div>
  <div class=researchBlock>${keyValue([["Length (bp)",o.length_bp],["Orientation semantics",o.orientation_semantics],["Semantic state",o.semantic_state],["Data completeness",o.data_completeness],["Discovery experiment",o.discovery_experiment_id],["Source artifact",o.source_artifact_id]])}</div>
  ${o.sequence?`<div><h3>Exact released sequence</h3><div class=seq>${esc(o.sequence)}</div><div class=muted>SHA-256 ${esc(o.sequence_sha256)}</div></div>`:`<div class="researchBlock callout warn"><b>Sequence not populated.</b> ${esc(o.data_completeness)}. Missing data stays missing rather than being reconstructed.</div>`}
  </div>
  <div class=learnBlock><div class=card><h3>Post-freeze interpretation</h3>${anns.length?anns.map(a=>`<p>${esc(a.annotation_value)}<br><span class=muted>${esc(a.annotation_type)} · ${esc(a.evidence_state)}</span></p>`).join(""):"<p class=muted>No post-freeze annotation stored.</p>"}</div></div>`;
 } else if(tab==="locations"){html+=occurrencePanel(o.object_id)} else if(tab==="connections"){html+=`<div class=card><h3>Connections</h3>${edgeTable(o.object_id,true)}</div>`}
 else if(tab==="evidence"){html+=`<div class=card><h3>Evidence path</h3>${trail(o,ex,art)}</div>`}
 else if(tab==="graph"){html+=graph(o.object_id)}
 else if(tab==="measurements"){html+=`<div class=card><h3>Measurements for this object</h3>${measurementTable(S.measurements.filter(m=>m.subject_type==="OBJECT"&&m.subject_id===o.object_id))}</div><div class=card><h3>Measurements from its discovery experiment</h3>${measurementTable(S.measurements.filter(m=>m.subject_type==="EXPERIMENT"&&m.subject_id===o.discovery_experiment_id))}</div>`}
 else if(tab==="provenance"){html+=`<div class=card><h3>Source chain</h3><ul>${provenancePath(o.source_artifact_id)}</ul></div>`;html+=`<div class=card><h3>Reverse provenance</h3>${trail(o,ex,art)}</div><div class=card><h3>Artifact record</h3><pre>${esc(JSON.stringify(art,null,2))}</pre></div>`}
 else html+=`<div class=card><h3>Raw Codebook record</h3><pre>${esc(JSON.stringify(o,null,2))}</pre></div>`;
 $("content").innerHTML=html;document.querySelectorAll("[data-tab]").forEach(b=>b.onclick=()=>{tab=b.dataset.tab;renderObject()});document.querySelectorAll("[data-goto-object]").forEach(b=>b.onclick=e=>{e.preventDefault();selectObject(b.dataset.gotoObject)});bindTerms();
}
function edgeTable(id,human){
 const es=S.edges.filter(e=>e.source_object_id===id||e.target_object_id===id);if(!es.length)return "<p class=muted>No graph edges stored for this object.</p>";
 const names={CONTAINS:"contains",HAS_MEMBER:"has member",ORDERED_NEIGHBORHOOD:"appears in an ordered neighborhood with",EXACT_COLINEAR_SPACING:"keeps the same exact spacing relationship with"};
 return `<table><tr><th>Relationship</th><th>Other object</th><th>Distance</th><th>Evidence</th></tr>${es.map(e=>{const other=e.source_object_id===id?e.target_object_id:e.source_object_id,dist=e.exact_distance_bp??(e.min_distance_bp!=null?`${e.min_distance_bp}–${e.max_distance_bp} bp`:"—");return `<tr><td>${esc(human?(e.target_object_id===id?({CONTAINS:"is inside",HAS_MEMBER:"is a member of",ORDERED_NEIGHBORHOOD:"appears after",EXACT_COLINEAR_SPACING:"appears after"}[e.edge_type]||e.edge_type):(names[e.edge_type]||e.edge_type)):e.edge_type)}</td><td><a href="#" data-goto-object="${esc(other)}">${esc(other)}</a></td><td>${esc(dist)}</td><td>${esc(e.evidence_state)}</td></tr>`}).join("")}</table>`;
}
function trail(o,ex,art){return `<ol><li><b>Source artifact</b> — ${esc(art?.name||o.source_artifact_id)}</li><li><b>Experiment</b> — ${esc(ex?.experiment_id||o.discovery_experiment_id)} · ${esc(ex?.title||"")}</li><li><b>Codebook object</b> — ${esc(o.object_id)} · ${esc(o.evidence_state)}</li><li><b>Interface</b> — this page renders that released record.</li></ol><p class=muted>${term("provenance","Provenance")} means being able to trace a displayed statement back toward its source.</p>`}
function measurementTable(ms){if(!ms.length)return "<p class=muted>No measurements stored for this subject.</p>";return `<table><tr><th>Metric</th><th>Value</th><th>Unit</th><th>Notes</th></tr>${ms.map(m=>`<tr><td>${esc(m.metric)}</td><td>${fmt(m.value_num??m.value_text)}</td><td>${fmt(m.unit)}</td><td>${fmt(m.notes)}</td></tr>`).join("")}</table>`}
function graph(root){
 const es=S.edges.filter(e=>e.source_object_id===root||e.target_object_id===root),ids=[root,...new Set(es.flatMap(e=>[e.source_object_id,e.target_object_id]).filter(x=>x!==root))],W=900,H=410,cx=450,cy=200,R=145,pos={[root]:[cx,cy]};
 ids.slice(1).forEach((id,i)=>{const a=2*Math.PI*i/Math.max(1,ids.length-1)-Math.PI/2;pos[id]=[cx+Math.cos(a)*R,cy+Math.sin(a)*R]});
 const lines=es.map(e=>{const a=pos[e.source_object_id],b=pos[e.target_object_id];return `<line class=edge x1=${a[0]} y1=${a[1]} x2=${b[0]} y2=${b[1]}><title>${esc(e.edge_type)}</title></line>`}).join("");
 const nodes=ids.map(id=>{const [x,y]=pos[id];return `<g class=node data-node="${esc(id)}" style="cursor:pointer"><circle cx=${x} cy=${y} r=${id===root?35:29}></circle><text x=${x} y=${y+4} text-anchor=middle>${esc(id.length>17?id.slice(0,15)+"…":id)}</text></g>`}).join("");
 setTimeout(()=>document.querySelectorAll("[data-node]").forEach(n=>n.onclick=()=>selectObject(n.dataset.node)),0);return `<div class=card><h3>Immediate evidence graph</h3><svg class=graph viewBox="0 0 ${W} ${H}"><defs><marker id=arrow markerWidth=8 markerHeight=8 refX=7 refY=3 orient=auto><path d="M0,0 L0,6 L7,3 z" fill="#617989"/></marker></defs>${lines}${nodes}</svg>${edgeTable(root,true)}</div>`;
}
function experiments(){
 const plainExp={"PC-0001":"Can exact DNA pieces and their neighborhood be recovered across three very different domains without using gene labels?","PC-0002":"Can a blind search recover a conserved coding pattern in E. coli and yeast?","CAL-VOCAB":"How quickly does exact shared DNA vocabulary thin out as the word length gets longer?","CAL-EXACTGAP":"Does the same exact gap between two pieces transfer to a held-out domain?","CAL-ORDERWIN":"Does a looser A-before-B window transfer to a held-out domain?","CAL-COMPRESS":"Is one flat exact dictionary a good compression model?"};
 $("content").innerHTML=`<div class=hero><div class=eyebrow>Experiments</div><h2>Every experiment should answer a question—even when the answer is “no.”</h2><p>Positive proof cases and negative calibrations are shown together.</p></div>${S.experiments.map(e=>{const n=S.measurements.filter(m=>m.subject_type==="EXPERIMENT"&&m.subject_id===e.experiment_id).length;return `<div class=finding><div class=question>${esc(e.experiment_id)}</div><h3>${esc(plainExp[e.experiment_id]||e.title)}</h3><p class=learnBlock>${esc(e.title)}</p><div class=badges>${badge(e.status,e.status.includes("NEGATIVE")?"bad":"good")}${badge("TIER "+e.evidence_tier)}${badge(e.annotation_blind?"ANNOTATION-BLIND":"ANNOTATED")}</div><p class=muted>${n} stored measurements</p><button class=action data-exp="${esc(e.experiment_id)}">Open experiment</button></div>`}).join("")}`;
 document.querySelectorAll("[data-exp]").forEach(b=>b.onclick=()=>experimentDetail(b.dataset.exp));
}
function experimentDetail(id){const e=expById[id],ms=S.measurements.filter(m=>m.subject_type==="EXPERIMENT"&&m.subject_id===id);$("content").innerHTML=`<button class=tab id=backExp>← Experiments</button><div class=card><h2>${esc(e.title)}</h2><div class=badges>${badge(e.status)}${badge("TIER "+e.evidence_tier)}</div><div class=learnBlock>${keyValue([["Experiment ID",e.experiment_id],["Date",e.experiment_date],["Reveal state",e.reveal_state],["Annotation blind",e.annotation_blind]])}</div></div><div class=card><h3>Measurements (${ms.length})</h3>${measurementTable(ms)}</div><div class=researchBlock><div class=card><h3>Raw experiment record</h3><pre>${esc(JSON.stringify(e,null,2))}</pre></div></div>`;$("backExp").onclick=experiments}
function vocabRows(){const ms=S.measurements.filter(m=>m.subject_id==="CAL-VOCAB"&&m.metric.startsWith("shared_exact_kmers_")),byK={};ms.forEach(m=>{const z=/k=(\d+)/.exec(m.notes||"");if(!z)return;(byK[+z[1]]??={})[m.metric]=m.value_num});return Object.entries(byK).map(([k,v])=>({k:+k,...v})).sort((a,b)=>a.k-b.k)}
function vocabulary(){
 const rows=vocabRows(),max=Math.max(...rows.map(r=>r.shared_exact_kmers_all_three||0)),w=v=>v<=0?0:Math.max(2,Math.log10(v+1)/Math.log10(max+1)*100);
 $("content").innerHTML=`<div class=hero><div class=eyebrow>DNA vocabulary</div><h2>How long can an exact shared DNA “word” get before the common vocabulary almost disappears?</h2><p>A ${term("k-mer","k-mer")} is simply a DNA word exactly <i>k</i> letters long. The bars below show words shared by all three pilot domains.</p></div>
 <div class=card><div class=question>Read the pattern before the numbers</div><p>Short words are extremely common. As the exact word length rises, the all-three shared set collapses rapidly. At k=16, 54 exact words remain; at k=18, none remain across all three pilot genomes.</p>${rows.map(r=>`<div class=vocabRow><b>k=${r.k}</b><div class=bartrack title="${comma(r.shared_exact_kmers_all_three||0)}"><div class=bar style="width:${w(r.shared_exact_kmers_all_three||0)}%"></div></div><span>${comma(r.shared_exact_kmers_all_three||0)}</span></div>`).join("")}</div>
 <div class=learnBlock><div class=card><h3>Why this is only a calibration</h3><p>The result describes this frozen pilot dataset and this exact-match representation. It does not establish a universal biological word length.</p></div></div>
 <div class=researchBlock><div class=card><h3>Pairwise counts</h3><table><tr><th>k</th><th>E. coli ↔ Pyrococcus</th><th>E. coli ↔ yeast</th><th>Pyrococcus ↔ yeast</th><th>All three</th></tr>${rows.map(r=>`<tr><td>${r.k}</td><td>${comma(r.shared_exact_kmers_ecoli_pyro||0)}</td><td>${comma(r.shared_exact_kmers_ecoli_yeast||0)}</td><td>${comma(r.shared_exact_kmers_pyro_yeast||0)}</td><td>${comma(r.shared_exact_kmers_all_three||0)}</td></tr>`).join("")}</table></div></div>`;
 bindTerms();
}
function models(){
 const ow=["training=ECOLI+PYRO; heldout=YEAST","training=ECOLI+YEAST; heldout=PYRO","training=PYRO+YEAST; heldout=ECOLI"];
 const compression=measures("CAL-COMPRESS");
 const groups={};compression.forEach(m=>{const k=(m.notes||"");(groups[k]??={notes:k})[m.metric]=m.value_num});
 $("content").innerHTML=`<div class=hero><div class=eyebrow>What failed</div><h2>Wrong models are useful when we keep them.</h2><p>LIFE-CODE stores falsified representations as first-class evidence. That narrows the space of explanations without rewriting the rules after seeing the answer.</p></div>
 <div class=storygrid>
  <div class=story><div class=question>Flat dictionary</div><h3>Exact words alone did not pay for themselves.</h3><p>Across the tested fixed-length dictionaries, no valid configuration beat raw 2-bit/base coding after dictionary/reference costs.</p><div class=learnBlock><p>The strongest-looking coverage values occurred at shorter k, but the dictionary overhead erased the apparent gain.</p></div></div>
  <div class=story><div class=question>Exact gap</div><h3>“Keep exactly the same distance” did not transfer.</h3><p>Exact A→B gap structure produced zero held-out deep-domain modules in every pilot fold.</p></div>
  <div class=story><div class=question>Ordered 10 kb window</div><h3>Even a looser neighborhood rule still failed held-out transfer.</h3>${ow.map(n=>`<div class=simpleRow><b>${esc(n.replace('training=','train ').replace('; heldout=',' → holdout '))}</b><span>${comma(mval("CAL-ORDERWIN","training_modules",n))} training modules → <b>${comma(mval("CAL-ORDERWIN","transferred_modules",n))} transferred</b></span></div>`).join("")}<div class=callout><b>Null check:</b> ${comma(mval("CAL-ORDERWIN","complete_shuffled_null_genomes"))} complete shuffled held-out null genomes also produced ${comma(mval("CAL-ORDERWIN","transferred_modules_across_all_nulls"))} transferred modules.</div></div>
 </div>
 <div class=researchBlock><div class=card><h3>Flat-dictionary calibration table</h3><table><tr><th>Training / holdout / k</th><th>coverage %</th><th>dictionary entries</th><th>used in holdout</th><th>full overhead %</th><th>oracle overhead %</th></tr>${Object.values(groups).map(g=>`<tr><td>${esc(g.notes)}</td><td>${fmt(g.coverage_percent)}</td><td>${fmt(g.dictionary_entries)}</td><td>${fmt(g.used_in_heldout)}</td><td>${fmt(g.full_vs_raw_overhead_percent)}</td><td>${fmt(g.oracle_vs_raw_overhead_percent)}</td></tr>`).join("")}</table></div></div>`;
}
function program(){const bench=P.benchmarks||[],lad=P.prediction_maturity_ladder||[],hist=P.program_history||[];$("content").innerHTML=`<div class=hero><div class=eyebrow>Roadmap</div><h2>LIFE-CODE is being built as a chain: evidence first, interpretation later, prediction last.</h2><p>This view separates what is live, what is built as infrastructure, what remains sealed, and what still requires verified recovery or testing.</p></div><div class=card><div class=question>Four canonical pillars</div><div class=pillargrid>${(F.pillars||[]).map(x=>`<div class=pillar><div class=pid>${esc(x.id)}</div><h3>${esc(x.question)}</h3><p>${esc(x.plain)}</p><button class=action data-route="${esc(x.route)}">Open ${esc(x.id.toLowerCase())} →</button></div>`).join("")}</div></div><div class=card><h3>Where the project actually stands</h3>${frontier()}</div><div class=card><div class=question>Whole-program flow</div><div class=pipeline>${(P.core_flow||[]).map(x=>`<div class=pipe>${esc(x)}</div>`).join("")}</div><p class=learnBlock>Evidence enters first. History and trait interpretation happen downstream. Constraints decide which states are plausible. Visualization is last and cannot upgrade weak evidence into a stronger scientific claim.</p></div><div class=storygrid><div class=story><div class=statusnote>built contract · not a result</div><h3>Retrodiction before extrapolation</h3><p>Before LIFE-CODE is allowed to predict an unobserved biological state, it must first predict a real state that was deliberately hidden until after the prediction was frozen.</p></div><div class=story><div class=statusnote>built contract · not a result</div><h3>The packet, not the picture</h3><p>A visual can be compelling and still scientifically unsupported. The machine-readable prediction packet carries the claim; the renderer only visualizes it.</p></div><div class=story><div class=statusnote>built contract · not a result</div><h3>The pixel needs provenance</h3><p>Every scientifically meaningful visual region must trace back to a frozen prediction channel. Unsupported detail must be marked artistic-only, ghosted, or omitted.</p></div><div class=story><div class=statusnote>built contract · not a result</div><h3>Biological Diff</h3><p>The framework includes a machine-readable diff layer intended to compare biological states or branches, preserve uncertainty, and test recurrent changes across independent contrasts.</p></div></div><div class=card><h3>Prediction maturity ladder</h3><div class=ladder>${lad.map(x=>`<div class=rung><span class=lvl>${esc(x.level)}</span><span class=name>${esc(x.name)}</span><span class=req>${esc(x.requirement)}</span></div>`).join("")}</div></div><div class=card><h3>Real benchmark bridges already designed</h3>${bench.map(b=>`<div class=finding><div class=statusnote>${esc(b.status)}</div><h3>${esc(b.benchmark_id)} · ${esc(b.name)}</h3><p>${esc(b.purpose)}</p>${b.published_cohort?`<div class=statstrip><div class=stat><b>${b.published_cohort.n_total}</b><span>published subjects</span></div><div class=stat><b>${b.published_cohort.yellow} / ${b.published_cohort.white}</b><span>yellow / white male forewing phenotypes</span></div><div class=stat><b>${b.frozen_split_contract.expected_train.total} / ${b.frozen_split_contract.expected_holdout.total}</b><span>planned train / sealed holdout</span></div></div>`:""}${b.panel_summary?`<div class=statstrip><div class=stat><b>${b.panel_summary.published_study_species}</b><span>rockfish species in source study</span></div><div class=stat><b>${b.panel_summary.extreme_panel_species}</b><span>extreme-panel species</span></div><div class=stat><b>${b.panel_summary.independent_trait_shifts}</b><span>independent trait shifts represented in design context</span></div></div>`:""}<div class=sourcebox>Program source: <a href="program_sources/${esc(b.source_file)}">${esc(b.source_file)}</a></div></div>`).join("")}</div><div class=card><h3>Build history</h3><div class=timeline>${hist.map(x=>`<div class=mile><h3>${esc(x.version)} · ${esc(x.title)}</h3><div class=mstate>${esc(x.state)}</div><p>${esc(x.summary)}</p></div>`).join("")}</div></div><div class=researchBlock><div class=card><h3>Program source manifest</h3><table><tr><th>File</th><th>Bytes</th><th>SHA-256</th></tr>${(P.sources||[]).map(s=>`<tr><td><a href="program_sources/${esc(s.file)}">${esc(s.file)}</a></td><td>${comma(s.bytes)}</td><td><code>${esc(s.sha256)}</code></td></tr>`).join("")}</table></div></div>`;bindTerms();}
function evidenceLegend(){return `<div class=stategrid>${(F.evidence_states||[]).map(x=>`<div class=statecard><b>${esc(x.id.replaceAll("_"," "))}</b><span>${esc(lens==="research"?x.research:x.plain)}</span></div>`).join("")}</div>`;}
function evolutionaryHistory(){const hs=F.history_edge_types||[],hp=F.history_public_state||{};$("content").innerHTML=`<div class=hero><div class=eyebrow>HISTORY · How did it get here?</div><h2>A genome is not a clean blueprint. It is a living history that has been copied, edited, duplicated, moved, merged—and partly erased.</h2><p class=answer>LIFE-CODE's history layer is designed to represent competing evolutionary explanations without pretending sequence persistence automatically tells us what happened.</p></div><div class=card><div class=question>What is actually released today?</div><div class=statstrip><div class=stat><b>${comma(hp.released_structural_edges??0)}</b><span>released structural Codebook edges</span></div><div class=stat><b>${comma(hp.released_object_specific_history_edges??0)}</b><span>released object-specific history-edge assertions</span></div></div><div class=callout><b>No invented history.</b> ${esc(hp.note||"")}</div></div><div class=card><h3>History is more than a family tree</h3><p>Some changes are ordinary parent-to-descendant inheritance. Others can involve duplication, loss, rearrangement, mobile DNA, horizontal transfer, or ancient biological mergers. LIFE-CODE therefore treats history as an evidence-labeled network rather than forcing every object into one story.</p><div class=historygrid>${hs.map(x=>`<div class=historyevent><div class=hid>${esc(x.id)}</div><h3>${esc(x.plain)}</h3><p class=learnBlock>${esc(x.research)}</p><div class="rule researchBlock">${esc(x.certainty_rule)}</div></div>`).join("")}</div></div><div class=card><h3>The rule that prevents overclaiming</h3><p>${esc(F.genome_history_rule||"")}</p><div class=learnBlock><ul>${(F.anti_overclaim||[]).map(x=>`<li>${esc(x)}</li>`).join("")}</ul></div></div><div class=card><h3>How a history claim should earn its way into the Codebook</h3><div class=stepbar><div class=step><b>1 · Observe structure</b>Record sequence and physical relationships.</div><div class=step><b>2 · Compare lineages</b>Measure where the structure persists, changes, or disappears.</div><div class=step><b>3 · Test alternatives</b>Compete inheritance, duplication, transfer, loss, artifact and other explanations.</div><div class=step><b>4 · Store uncertainty</b>Attach a typed history edge only at the evidence level earned.</div></div></div><div class=researchBlock><div class=card><h3>Framework source</h3>${keyValue([["Source",F.source_file],["SHA-256",F.source_sha256],["Framework context schema",F.schema]])}<div class=downloads><a href="program_sources/${esc(F.source_file)}">Canonical framework source</a><a href="data/LIFE_CODE_FRAMEWORK_CONTEXT_v0.10.json" download>Framework context JSON</a></div></div></div>`;}
function resilience(){const q={"attack surface":"Where can a harmful process enter or gain leverage?","dependency chain":"What else breaks if this component fails?","redundancy":"What alternate mechanism can carry the load?","control/privilege boundary":"Which control points can change many downstream states?","integrity checking":"How does the system detect or repair errors?","rollback/recovery":"How does the system restore function after damage?","legacy code":"Which inherited structures remain because newer biology was built around them?","exploit":"How can a disease process hijack normal machinery?","fault tolerance":"How much disruption can the system absorb before function collapses?"};const b=(P.benchmarks||[]).find(x=>x.benchmark_id==="BENCH-R01");$("content").innerHTML=`<div class=hero><div class=eyebrow>RESILIENCE · How does life survive failure?</div><h2>Instead of asking only “which gene causes this?”, ask where failure enters, what depends on that component, what backups exist, and how other lineages solved similar problems.</h2><p class=answer>This is a systems lens for comparative biology—not a claim that cells literally run computer-security software.</p></div><div class=securitygrid>${(F.systems_security_lens||[]).map(x=>`<div class=security><h3>${esc(x)}</h3><p>${esc(q[x]||"Comparative systems question.")}</p></div>`).join("")}</div><div class=callout><b>Analogy boundary:</b> the security language is a questioning tool. It does not turn metaphor into mechanism.</div>${b?`<div class=card><div class=statusnote>${esc(b.status)}</div><h3>${esc(b.benchmark_id)} · ${esc(b.name)}</h3><p>${esc(b.purpose)}</p><div class=statstrip><div class=stat><b>${comma(b.panel_summary?.published_study_species||0)}</b><span>species in published source study</span></div><div class=stat><b>${comma(b.panel_summary?.extreme_panel_species||0)}</b><span>extreme-panel species in benchmark design</span></div><div class=stat><b>${comma(b.panel_summary?.independent_trait_shifts||0)}</b><span>independent trait shifts represented in design context</span></div></div><div class=callout><b>Not a longevity result.</b> This is benchmark architecture intended to test whether repeated independent branch contrasts recover recurrent subsystems before semantic reveal.</div><div class=researchBlock><pre>${esc(JSON.stringify(b.analysis_strategy,null,2))}</pre></div></div>`:""}<div class=card><h3>Why repeated evolution matters</h3><p>If closely related lineages independently move toward similar traits, each branch can act like a natural comparison. Repeated changes can help distinguish a recurrent subsystem from one lineage's historical accident—but only with phylogenetic, environmental, body-size, composition and other controls.</p></div>`;}
function frontier(){return `<div class=frontier>${(F.frontier||[]).map(x=>`<div class=frontrow><div class=frontname>${esc(x.name)}</div><div class=frontstate>${esc(x.state)}</div><div class=frontdetail>${esc(x.plain)}<small>${esc(x.detail)}</small></div></div>`).join("")}</div>`;}
function claims(){
 $("content").innerHTML=`<div class=hero><div class=eyebrow>What we can claim</div><h2>The boundary is part of the result.</h2><p>Every released claim carries a line it is not allowed to cross.</p></div><div class=card><h3>How LIFE-CODE labels evidence</h3>${evidenceLegend()}</div>${S.claims.map(c=>`<div class=finding><div class=badges>${badge(c.evidence_state,c.evidence_state==="FALSIFIED"?"bad":"good")}${badge(c.status)}</div><h3>${esc(c.claim_text)}</h3><div class=callout><b>Boundary:</b> ${esc(c.boundary_text||"—")}</div><div class=researchBlock><code>${esc(c.claim_id)}</code></div></div>`).join("")}`;
}
function glossary(){
 $("content").innerHTML=`<div class=hero><div class=eyebrow>Glossary</div><h2>You should not need a genetics degree to navigate the evidence.</h2><p>These definitions explain how LIFE-CODE uses each term. Research mode still exposes the exact database language.</p></div><div class=glossarygrid>${Object.entries(GLOSSARY).map(([k,v])=>`<div class=term><h3>${esc(k)}</h3><p>${esc(v)}</p></div>`).join("")}</div>`;
}
function integrity(){
 const checks=S.public_release_gates.checks||{};$("content").innerHTML=`<div class=hero><div class=eyebrow>Verify it</div><h2>Trust the evidence path, not the presentation.</h2><p>This page exposes the released source hashes and the firewall that keeps unreleased experiment outcomes out of the public layer.</p></div>
 <div class=grid><div class=metric><div class=n>${S.public_release_gates.passed?"PASS":"FAIL"}</div><div class=l>public release gate</div></div><div class=metric><div class=n>${Object.values(checks).reduce((a,b)=>a+Number(b),0)}</div><div class=l>blocked-record count</div></div><div class=metric><div class=n>${S.counts.artifacts}</div><div class=l>source artifacts</div></div></div>
 <div class=card><h3>Source integrity</h3>${keyValue([["Source database",S.source_database.filename],["Source database SHA-256",S.source_database.sha256],["Snapshot schema",S.snapshot_schema],["Generated UTC",S.generated_utc]])}</div>
 <div class=card><h3>Public firewall</h3>${keyValue(Object.entries(checks))}<p>${esc(S.public_release_gates.rule)}</p></div>
 <div class=card><h3>Visual truth states</h3><p>A scientific display must say what kind of thing it is showing. A beautiful render cannot silently become evidence.</p><div class=truthgrid>${(F.visual_truth_states||[]).map(x=>`<div class=truth><b>${esc(x.id)}</b><span>${esc(x.plain)}</span></div>`).join("")}</div></div>
 <div class=card><h3>Known open reconciliation items</h3><ul><li>PC0001 literals, 19 focused locations, and all 54 shared 16-base vocabulary records are now reconciled. The remainder of the historical research graph is still pending.</li><li>The older Proof Case 0001 k=16 null summary and the later full vocabulary-ladder k=16 summary require source-level reconciliation.</li></ul></div>
 <div class=downloads><a href="data/LIFE_CODE_PUBLIC_CODEBOOK_v0.10.json" download>Download public JSON</a><a href="downloads/LIFE_CODE_CODEBOOK_CORE_v0.10.sqlite" download>Download SQLite Codebook</a><a href="SCIENTIFIC_RELEASE_POLICY.md">Release policy</a></div>`;
}
function render(){if(view==="home")home();else if(view==="findings")findings();else if(view==="recovery")evidenceRecovery();else if(view==="codebook")current?renderObject():objectLanding();else if(view==="experiments")experiments();else if(view==="models")models();else if(view==="vocabulary")vocabulary();else if(view==="history")evolutionaryHistory();else if(view==="resilience")resilience();else if(view==="program")program();else if(view==="claims")claims();else if(view==="glossary")glossary();else integrity();bindTerms()}
$("exploreLens").onclick=()=>setLens("explore");$("learnLens").onclick=()=>setLens("learn");$("researchLens").onclick=()=>setLens("research");
document.querySelectorAll("[data-view]").forEach(b=>b.onclick=()=>setView(b.dataset.view));
["search","type","state"].forEach(id=>$(id).addEventListener(id==="search"?"input":"change",renderList));
initFilters();renderList();setLens(lens);setExplorer(false);$("footerVersion").textContent=`${S.snapshot_schema} · Interface ${window.LIFE_CODE_INTERFACE_VERSION}`;

const requestedObject=new URLSearchParams(location.hash.slice(1)).get("object");if(requestedObject)selectObject(requestedObject);
