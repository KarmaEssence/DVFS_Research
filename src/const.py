
# ------------Parametres de la generation de la CMTD  ------------------------------ */
b = 1e9 # Nombre d'instructions par tache.
CPI = 1  # Nombre de cycle par instructions que reçoit le processeur.
C = 20   # Nombre de coeurs du processeur  (i.e. serveurs) -> initial value 15, pour les test 3, 7 pour etre efficace
B = 45   # Nombre max de tâches en attente (i.e. Buffersize) -> initial value 50, pour les test 10, 20 pour etre efficace
Type = 1 # 0 : ne pas compter l'énergie au démarage, 1 : compter l'énergie au démarage

# ------------Parametres énergetiques : cas d'un processeur AMD  --------------------- */

fi = [1e9, 1.8 * 1e9, 2 * 1e9, 2.2 * 1e9, 2.4 * 1e9, 2.6 * 1e9] # fréquence en GHz.
Mu = [float(f / (b * CPI)) for f in fi] # taux de service par palier (i.e frequence)
en = [32, 55, 65, 76, 90, 95] # consommation d'un serveur allumé actif par palier
en_idle = [e/4 for e in en] # consommation d'un serveur allumé non-actif par palier (75% de reduction)
Es = en # côut de changement de get_pstate (get_pstate i vers get_pstate i+1) voir pour en/2 ou un équivalent
