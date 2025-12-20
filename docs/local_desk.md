# SQLITE3 Commands

sqlite3 data/sales_fulfillment.db -header -column "SELECT client_id, company_name, industry, service_type FROM submission;"



# Kubectl commands


kubectl get all -n sales-fulfillment  

kubectl get pods -n sales-fulfillment -w  

kubectl port-forward svc/frontend 7004:80 -n sales-fulfillment


# test scripts - local unit test 
source .venv/bin/activate

PYTHONPATH=. pytest tests/