
# create folder './logs' if not exist
mkdir -p logs

#!/bin/sh
celery -A aria.celery.core flower --address=localhost 1>logs/flower.log 2>logs/flower.log &
FLOWER=$!
celery -A aria.celery.core worker --loglevel=info 1>logs/worker.log 2>logs/worker.log & 
WORKER=$!
echo "${GREEN}Press CTRL+C to stop processes${RESET}"

running=true
GREEN="\e[32m"  # Vert
RED="\e[31m"    # Rouge
RESET="\e[0m" 

# Fonction pour gérer la sortie proprement lors de l'interruption CTRL+C
cleanup() {
    echo "${GREEN}Arrêt en cours de Celery Flower (PID : $FLOWER)...${RESET}"
    kill -TERM $FLOWER
    wait $FLOWER
    echo "Celery Flower a été arrêté."
    
    echo "${GREEN}Arrêt en cours de Celery Worker (PID : $WORKER)...${RESET}"
    kill -TERM $WORKER
    wait $WORKER
    echo "Celery Worker a été arrêté."

    # remove folder './logs' and all files
    rm -rf logs

    running=false
}

# Associer la fonction cleanup à SIGINT (CTRL+C)
trap cleanup SIGINT

while $running; do
    sleep 1
done