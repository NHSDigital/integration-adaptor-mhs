projects=("$@")

if [ -z "$projects" ]
then
    projects=( "mhs/common" "mhs/outbound" "mhs/inbound" "mhs/spineroutelookup" "integration-tests/integration_tests" "examples/SCR" "examples/SCRWebService )
fi

for i in "${projects[@]}"
do
    echo "-----------------------------"
    echo "--- Installing virtualenv in '$i'"
    echo "-----------------------------"
    (cd $i; pipenv --rm; pipenv install --dev --clear; pipenv update --clear)
done
