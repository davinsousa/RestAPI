import json

#updates the balance, including changes in borrower and lender
def up_balance(lender, borrower, amount, database):

	n=0
	for d in database["users"]:
		if d["name"]==lender:
			len_index=n
			dl=up_lender(lender, borrower, amount, d)
		else:
			if d["name"]==borrower:
				bor_index=n
				db=up_borrower(lender, borrower, amount, d)
		n=n+1

	if len_index<bor_index:
		return {"users":[dl, db]}
	else:
		return {"users":[db, dl]}
	
#updates lender information when a transaction is done
def up_lender(lender, borrower, amount, d):

	flag=""	

	if borrower in d["owes"]: #check if borrower already owes the lender
		
		am_exist=d["owes"][borrower]

		if am_exist > amount:
			d["owes"][borrower]=d["owes"][borrower]-amount
		else:
			if am_exist == amount:
				del d["owes"][borrower]
			else:
				del d["owes"][borrower]
				if borrower in d["owed_by"]:
					d["owed_by"][borrower]=d["owed_by"][borrower]+amount
				else:
					d["owed_by"][borrower]=amount-am_exist
	else:

		if borrower in d["owed_by"]:
			d["owed_by"][borrower]=d["owed_by"][borrower]+amount
		else:
			d["owed_by"][borrower]=amount

	d["balance"]=d["balance"]+amount

	return d

#updates borrower information when a transaction is done
def up_borrower(lender, borrower, amount, d):
	
	flag=""
	am_exist=0

	if lender in d["owed_by"]: #check if the lender owes money to borrower
		
		am_exist=d["owed_by"][lender]

		if am_exist > amount:
			d["owed_by"][lender]=d["owed_by"][lender]-amount
		else:
			if am_exist == amount:
				del d["owed_by"][lender]
			else:
				del d["owed_by"][lender]
				if lender in d["owes"]:
					d["owes"][lender]=d["owes"][lender]+amount-am_exist
				else:
					d["owes"][lender]=amount-am_exist
	else:

		if lender in d["owes"]:
			d["owes"][lender]=d["owes"][lender]+amount
		else:
			d["owes"][lender]=amount

	d["balance"]=d["balance"]-amount

	return d

class RestAPI:
	def __init__(self, database=None):
		self.database=database

	def get(self, url, payload=None):

		if payload is None:
			users_out=self.database["users"]
			return json.dumps({'users':users_out})
		else:
			list_users=json.loads(payload)["users"]
			out=[]
			for u in list_users:
				for d in self.database["users"]:
					if d["name"]==u:
						out.append(d)
			return json.dumps({"users":out})

	def post(self, url, payload=None):

		if url=="/add":
			d={"name":json.loads(payload)["user"], "owes":{}, "owed_by":{}, "balance":0.0}
			return json.dumps(d)
		
		if url=="/iou":
			json_f=json.loads(payload)
			result=up_balance(json_f["lender"],json_f["borrower"],json_f["amount"],self.database)
			return(json.dumps(result))


	
		
