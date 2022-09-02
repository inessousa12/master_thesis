if ! [ $(id -u) = 0 ]; then
   echo "The script need to be run as root." >&2
   exit 1
fi


if [ -x "$(command -v docker)" ]; then
    echo "docker is already installed"
else
    echo "docker must be installed. It will be installed next"
    #docker installation
    apt-get install curl
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
fi


docker-compose -f docker-compose.yaml up -d


echo ""
echo ""
docker container ps
echo ""
echo ""
echo "script execution: finished"

