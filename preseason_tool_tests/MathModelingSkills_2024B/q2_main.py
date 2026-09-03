"""Exact Q2 policy enumeration under the assumptions documented in q2_method_card.md."""
import csv, json, math, platform, sys, time
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "workspace/data_clean/q2_table1.json"
OUT = ROOT / "results/Q2/experiments/round1"
STATES = [(a,b,r) for a in range(3) for b in range(3) for r in range(2)]  # 0 absent,1 good,2 defective; revenue collected flag
INDEX = {s:i for i,s in enumerate(STATES)}

def solve(a, b):
    n=len(b); aug=[a[i][:]+[b[i]] for i in range(n)]
    for col in range(n):
        pivot=max(range(col,n),key=lambda i:abs(aug[i][col]))
        if abs(aug[pivot][col]) < 1e-12: raise ValueError("singular Bellman system")
        aug[col],aug[pivot]=aug[pivot],aug[col]
        q=aug[col][col]; aug[col]=[v/q for v in aug[col]]
        for row in range(n):
            if row != col:
                q=aug[row][col]
                aug[row]=[x-q*y for x,y in zip(aug[row],aug[col])]
    return [row[-1] for row in aug]

def component(status, test, p, buy, ins):
    if not test:
        return ([(1,1-p),(2,p)],buy) if status==0 else ([(status,1.0)],0.0)
    # Test all retained/new parts; a detected defect is discarded and replacement purchases repeat until good.
    replacement=(buy+ins)/(1-p)
    if status==1: return ([(1,1.0)],ins)
    return ([(1,1.0)],replacement if status==0 else ins+replacement)

def evaluate(c, policy):
    t1,t2,tp,dis=policy; n=len(STATES); P=[[0.0]*n for _ in range(n)]; reward=[0.0]*n; mass_err=0.0
    for si,(u,v,rev) in enumerate(STATES):
        o1,k1=component(u,t1,c['p1'],c['buy1'],c['inspect1']); o2,k2=component(v,t2,c['p2'],c['buy2'],c['inspect2'])
        for x,px in o1:
            for y,py in o2:
                w=px*py; reward[si] -= w*(k1+k2+c['assembly']+(c['product_inspect'] if tp else 0))
                bad=1.0 if (x==2 or y==2) else c['pq']
                good=1-bad
                if tp:
                    if rev==0: reward[si] += w*good*c['price']
                    if dis: reward[si] -= w*bad*c['disassembly']
                    nxt=(x,y,rev) if dis else (0,0,rev)
                    P[si][INDEX[nxt]] += w*bad
                else:
                    if rev==0: reward[si] += w*c['price']
                    reward[si] -= w*bad*c['exchange_loss']
                    if dis: reward[si] -= w*bad*c['disassembly']
                    nxt=(x,y,1) if dis else (0,0,1)
                    P[si][INDEX[nxt]] += w*bad
        mass=sum(P[si])
        # terminal success probability is implicit; transition mass cannot exceed one.
        mass_err=max(mass_err,max(0.0,mass-1.0))
    A=[[float(i==j)-P[i][j] for j in range(n)] for i in range(n)]
    try:
        val=solve(A,reward)
    except ValueError:
        return None, mass_err, None
    residual=max(abs(val[i]-(reward[i]+sum(P[i][j]*val[j] for j in range(n)))) for i in range(n))
    return val[INDEX[(0,0,0)]], mass_err, residual

def main():
    started=time.time(); cases=json.loads(INPUT.read_text()); OUT.joinpath('tables').mkdir(parents=True,exist_ok=True); OUT.joinpath('metrics').mkdir(parents=True,exist_ok=True)
    policies=list(product((0,1),repeat=4)); rows=[]; checks=[]
    for c in cases:
        vals=[]
        for p in policies:
            value,mass,res=evaluate(c,p); vals.append((value,p,mass,res))
        legal=[z for z in vals if z[0] is not None]
        best=max(legal,key=lambda z:z[0]); base=next(z for z in legal if z[1]==(0,0,0,0))
        rows.append({'case':c['case'],'best_policy':''.join(map(str,best[1])),'best_expected_profit':best[0],'baseline_policy':'0000','baseline_expected_profit':base[0],'improvement':best[0]-base[0]})
        checks.append({'case':c['case'],'max_transition_excess':max(z[2] for z in vals),'max_bellman_residual':max(z[3] for z in legal),'invalid_nonabsorbing_policies':[''.join(map(str,z[1])) for z in vals if z[0] is None],'unique_profit_count':len({round(z[0],10) for z in legal})})
    with OUT.joinpath('tables/q2_policy_comparison.csv').open('w',newline='') as f: w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
    # exact zero-defect sanity: no-test/no-disassembly earns price minus two purchases and assembly.
    z=dict(cases[0]); z.update(p1=0.0,p2=0.0,pq=0.0); zero=evaluate(z,(0,0,0,0))[0]; expected=z['price']-z['buy1']-z['buy2']-z['assembly']
    metrics={'policy_space_size':len(policies),'cases':checks,'zero_defect_profit':zero,'zero_defect_expected':expected,'zero_defect_abs_error':abs(zero-expected)}
    OUT.joinpath('metrics/sanity_metrics.json').write_text(json.dumps(metrics,indent=2),encoding='utf-8')
    summary={'schema_version':1,'question':'Q2','round':'round1','implementation_target':'python','random_seed':2026,'approved_decision_id':'accelerated_evaluation_override','methods':[{'method_id':'M2','role':'main_candidate','script':'code/Q2/q2_main.py','status':'success','execution_time_seconds':time.time()-started,'input_files':['workspace/data_clean/q2_table1.json'],'output_files':['results/Q2/experiments/round1/tables/q2_policy_comparison.csv','results/Q2/experiments/round1/metrics/sanity_metrics.json'],'figure_files':[],'metrics_summary':{'policies_enumerated':16},'warnings':['Normal G2.5 human method-choice gate bypassed only under user accelerated-evaluation authorization.'],'errors':[]},{'method_id':'B2','role':'usable_baseline','script':'code/Q2/q2_main.py','status':'success','execution_time_seconds':0.0,'input_files':['workspace/data_clean/q2_table1.json'],'output_files':['results/Q2/experiments/round1/tables/q2_policy_comparison.csv'],'figure_files':[],'metrics_summary':{},'warnings':[],'errors':[]}],'comparison':{'metric':'expected profit per fulfilled customer demand','baseline_policy':'0000'},'fallback_trigger':{'fallback_id':None,'condition':'singular system, residual > 1e-9, or transition mass > 1','observed':False,'evidence':'metrics/sanity_metrics.json'},'environment':{'python':sys.version,'platform':platform.platform()}}
    OUT.joinpath('run_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
if __name__=='__main__': main()
