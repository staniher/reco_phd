import pickle
from flask import Flask, request, render_template, jsonify
import numpy as np

app=Flask('__name__')
with open('BERTModel_RS.pkl', 'rb') as f:
    graduate_data=pickle.load(f)
#Acces à Background
liste_background=sorted([background['Background'] for background 
in graduate_data])

liste_bornwar=sorted(set([background['BornWar'] for background 
in graduate_data]))
liste_instLoc=sorted(set([background['InstitutionLocation'] for background 
in graduate_data]))
liste_SchoolWar=sorted(set([background['SchoolWar'] for background 
in graduate_data]))
liste_Family=sorted(set([background['Family'] for background 
in graduate_data]))
liste_PoliticianFam=sorted(set([background['PoliticianFam'] for background 
in graduate_data]))
liste_AdminstrativeFam=sorted(set([background['AdminstrativeFam'] for background 
in graduate_data]))
liste_CompanyFam=sorted(set([background['CompanyFam'] for background 
in graduate_data]))
liste_Degree=sorted(set([background['Degree'] for background 
in graduate_data]))

graduate_key_liste=[item['graduatekey'] for item in 
graduate_data]

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method=='POST':
		bw=request.form.get('BornWar')
		il=request.form.get('InstitutionLocation')
		sw=request.form.get('SchoolWar')
		fa=request.form.get('Family')
		pfa=request.form.get('PoliticianFam')
		adfa=request.form.get('AdminstrativeFam')
		comfa=request.form.get('CompanyFam')
		dg=request.form.get('Degree')
		select_metric='cosine'
		background=bw + ' '+ il + ' '+ sw + ' '+ fa +' '+ pfa +' '+adfa+ ' '+comfa +' '+dg
		try:
			selected_background=next(item for item in graduate_data if item['Background']
				==background)
			similar_backgrounds=[graduate_data[i] for i in selected_background[select_metric]]
			reco_employed=[e for e in similar_backgrounds if e['Employed']=='employed']
			return render_template('index.html',similar_backgrounds=reco_employed[:4] )
		except StopIteration:
			Cycle_No_Trouve=dg
			return render_template('index.html', resultat_no_trouver=Cycle_No_Trouve)
	else:
		return render_template('index.html',liste_bornwar=liste_bornwar,
		liste_instLoc=liste_instLoc,liste_SchoolWar=liste_SchoolWar,
		liste_Family=liste_Family,
		liste_PoliticianFam=liste_PoliticianFam,
		liste_AdminstrativeFam=liste_AdminstrativeFam,
		liste_CompanyFam=liste_CompanyFam,
		liste_Degree=liste_Degree
		 )

@app.route("/recommandations", methods=['GET'])
def get_recommandations():
	graduatekey=request.args.get('graduatekey', 
		default=None,type=str)
	num_reco=request.args.get("number", default=4, type=int)
	distance=request.args.get("distance", default='cosine', 
		type=str)
	champ=request.args.get('champ', default="graduatekey",
		type=str)
	if not graduatekey:
		return jsonify("Aucun background trouvé"), 400
	elif num_reco not in range(1,21):
		return jsonify("Les recommndations ne doivent être que moins de 5"),400
	elif graduatekey not in graduate_key_liste:
		return jsonify("Cette clé n'exixte pas"), 400
	elif champ not in graduate_data[0].keys():
		return jsonify("Le champ n'est pas dans le modèle"),400
	else:
		try:
			selected_background=next(item for item in 
				graduate_data if item['graduatekey']==graduatekey)
			similar_backgrounds=[graduate_data[i][champ] for i in selected_background[distance]]
			return jsonify(similar_backgrounds[:num_reco]), 200
		except Exception as e:
			return jsonify(str(e)), 500

if __name__=='__main__':
	app.run(debug=True)
		
