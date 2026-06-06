"""Gera o gráfico de churn e salva como PNG."""
import matplotlib
matplotlib.use("Agg")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

BG="#08071a"; CARD="#100f2e"; BORDER="#2a2560"
PINK="#f472b6"; CYAN="#38bdf8"; BLUE="#6366f1"
PURPLE="#a78bfa"; LAV="#818cf8"; TEXT="#ede9ff"; MUTED="#8b7ec8"
GREEN="#34d399"; YELLOW="#fbbf24"

plt.rcParams.update({
    "figure.facecolor": BG,"axes.facecolor": CARD,"axes.edgecolor": BORDER,
    "axes.labelcolor": MUTED,"axes.titlecolor": TEXT,"axes.titlesize": 13,
    "axes.labelsize": 10,"axes.titlepad": 14,"axes.spines.top": False,
    "axes.spines.right": False,"axes.grid": True,"grid.color": BORDER,
    "grid.linewidth": 0.6,"xtick.color": MUTED,"ytick.color": MUTED,
    "text.color": TEXT,"font.family": "DejaVu Sans",
    "legend.facecolor": CARD,"legend.edgecolor": BORDER,"legend.labelcolor": TEXT,
})

np.random.seed(42)
df = pd.DataFrame({
    "cliente_id": range(1,301),
    "idade": np.random.randint(18,60,300),
    "meses_ativo": np.random.randint(1,36,300),
    "suporte_contatos": np.random.randint(0,10,300),
    "uso_mensal_horas": np.random.uniform(1,50,300).round(1),
    "plano": np.random.choice(["Basic","Pro","Premium"],300),
    "churn": np.random.choice([0,1],300,p=[0.7,0.3])
})

fig,axs=plt.subplots(2,2,figsize=(14,9))
fig.patch.set_facecolor(BG)
fig.suptitle("Analise de Churn - App de Assinaturas",fontsize=17,fontweight="bold",color=PINK,y=1.01)

ax=axs[0,0]; ax.set_facecolor(CARD)
churn_pct=df["churn"].value_counts(normalize=True)*100
wedges,texts,autotexts=ax.pie(churn_pct,labels=None,autopct="%1.1f%%",
    colors=[CYAN,PINK],startangle=90,pctdistance=0.75,
    wedgeprops=dict(edgecolor=BG,linewidth=3,width=0.55))
for at in autotexts: at.set_fontsize(13); at.set_fontweight("bold"); at.set_color(TEXT)
ax.legend(["Ativo","Churn"],loc="center",fontsize=10,facecolor=CARD,edgecolor=BORDER,labelcolor=TEXT)
ax.text(0,0,f"{df['churn'].sum()}\ncancels",ha="center",va="center",fontsize=11,color=PINK,fontweight="bold")
ax.set_title("Taxa de Churn Geral",color=TEXT)

ax=axs[0,1]; ax.set_facecolor(CARD)
churn_plano=df.groupby("plano")["churn"].mean()*100
bars=ax.bar(churn_plano.index,churn_plano.values,color=[BLUE,PURPLE,CYAN],edgecolor="none",width=0.5)
for bar in bars:
    ax.text(bar.get_x()+bar.get_width()/2,bar.get_height()+0.4,f"{bar.get_height():.1f}%",
        ha="center",fontsize=11,fontweight="bold",color=TEXT)
ax.set_title("Churn por Plano (%)",color=TEXT); ax.set_ylabel("% Cancelamento",color=MUTED)
ax.spines["left"].set_color(BORDER); ax.spines["bottom"].set_color(BORDER)

ax=axs[1,0]; ax.set_facecolor(CARD)
ax.hist(df[df["churn"]==0]["uso_mensal_horas"],bins=15,color=CYAN,alpha=0.75,label="Ativo",edgecolor="none")
ax.hist(df[df["churn"]==1]["uso_mensal_horas"],bins=15,color=PINK,alpha=0.75,label="Churn",edgecolor="none")
ax.set_title("Uso Mensal vs Churn",color=TEXT); ax.set_xlabel("Horas por mes",color=MUTED)
ax.set_ylabel("Clientes",color=MUTED); ax.legend(fontsize=9)
ax.spines["left"].set_color(BORDER); ax.spines["bottom"].set_color(BORDER)

ax=axs[1,1]; ax.set_facecolor(CARD)
churn_tempo=df.groupby("churn")["meses_ativo"].mean()
bars=ax.barh(["Ativo","Churn"],churn_tempo.values,color=[CYAN,PINK],edgecolor="none",height=0.45)
for i,v in enumerate(churn_tempo.values):
    ax.text(v+0.3,i,f"{v:.1f} meses",va="center",fontsize=11,fontweight="bold",color=TEXT)
ax.set_title("Tempo Medio Ativo vs Churn",color=TEXT); ax.set_xlabel("Media de meses",color=MUTED)
ax.spines["left"].set_color(BORDER); ax.spines["bottom"].set_color(BORDER)

plt.tight_layout(pad=2.0)
plt.savefig("churn_analysis.png",dpi=150,bbox_inches="tight",facecolor=BG); plt.close()
print("Grafico salvo: churn_analysis.png")
