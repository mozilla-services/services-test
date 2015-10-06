# grab test manifest by product type:
#   curl -O https://raw.githubusercontent.com/mozilla-services/services-test/master/{{product}}/manifest.json
# test_type == security
# env == 'dev' | 'stage' | 'pre-prod' | 'prod' (but probably not prod ever)

if [ "$#" -ne 1 ]; then
  echo "Illegal number of parameters"
  echo "Usage: $ $0 {{url}}"
  exit
fi

make url="$1" run_docker
