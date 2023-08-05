DIR=`dirname $0`
docker build -t vonx-test -f "$DIR/Dockerfile" "$DIR/.." || exit 1
docker run --rm  -v vonx-test-wallet:/home/indy/.indy_client/wallet \
  -e "LOG_LEVEL=${LOG_LEVEL:-INFO}" \
  -ti vonx-test python -m test."${TEST:-testSequence}"
