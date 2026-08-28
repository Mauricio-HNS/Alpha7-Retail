import React from 'react';
import { createRoot } from 'react-dom/client';
import './styles.css';

type Recommendation = { sku:string; name:string; stock:number; sales:number; quantity:number; cost:number; urgency:'critical'|'high'|'normal' };
const data: Recommendation[] = [
 {sku:'SUT-2048-PRETO-40',name:'Sutiã Rendado Preto - 40',stock:7,sales:82,quantity:30,cost:246,urgency:'critical'},
 {sku:'CAL-109-BRANCO-M',name:'Calcinha Conforto Branca - M',stock:12,sales:51,quantity:18,cost:90,urgency:'high'},
 {sku:'BODY-77-PRETO-G',name:'Body Elegance Preto - G',stock:4,sales:40,quantity:22,cost:308,urgency:'critical'},
];
function App(){
 const total=data.reduce((s,x)=>s+x.cost,0);
 return <div className="app"><aside><div className="logo">A7<span>RETAIL</span></div>{['Dashboard','Produtos','Estoque','Vendas','Fornecedores','Compras','Recomendações IA','Aprovações','Relatórios','Configurações'].map((x,i)=><div className={'nav '+(!i?'active':'')}>{x}</div>)}<div className="footer">ALPHA7 AI<br/><small>Retail Intelligence</small></div></aside><main><header><div><h1>Visão Geral</h1><p>Compras e estoque inteligente</p></div><button>+ Nova compra</button></header><section className="cards"><Card label="Vendas do mês" value="€48.920" sub="+12,4% vs. mês anterior"/><Card label="Produtos em estoque" value="2.841" sub="37 abaixo do mínimo"/><Card label="Compra recomendada" value={'€'+total.toLocaleString('pt-PT')} sub="3 produtos prioritários"/><Card label="Aprovações" value="3" sub="Aguardando decisão"/></section><section className="panel"><div className="panelHead"><div><h2>Recomendações da IA</h2><p>Reposição calculada por vendas, estoque e prazo do fornecedor.</p></div><button className="ghost">Ver todas</button></div><table><thead><tr><th>Produto</th><th>SKU</th><th>Estoque</th><th>Vendas 30d</th><th>Comprar</th><th>Investimento</th><th>Status</th><th></th></tr></thead><tbody>{data.map(x=><tr><td><b>{x.name}</b></td><td>{x.sku}</td><td>{x.stock}</td><td>{x.sales}</td><td><b>{x.quantity}</b></td><td>€{x.cost}</td><td><span className={'badge '+x.urgency}>{x.urgency==='critical'?'Crítico':'Prioridade alta'}</span></td><td><button className="approve">Aprovar</button></td></tr>)}</tbody></table></section><section className="grid"><div className="panel"><h2>Insight Alpha7</h2><p className="insight">Produtos pretos estão vendendo 23% mais rápido nas últimas quatro semanas. O tamanho 40 apresenta maior risco de ruptura.</p></div><div className="panel"><h2>Fluxo de compra</h2><div className="flow">Estoque <b>→</b> Previsão <b>→</b> Recomendação <b>→</b> Aprovação <b>→</b> Pedido</div></div></section></main></div>
}
function Card(p:{label:string;value:string;sub:string}){return <div className="card"><p>{p.label}</p><strong>{p.value}</strong><small>{p.sub}</small></div>}
createRoot(document.getElementById('root')!).render(<App/>);
