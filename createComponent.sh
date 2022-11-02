echo "Creating component folder"
if [ -d "$1" ]; then
  echo "Component existed!!!"
else

  mkdir project/api/"$1"
  touch project/api/"$1"/__init__.py
  touch project/api/"$1"/"$1_views.py"
  touch project/api/"$1"/"$1_helper.py"
  touch project/api/"$1"/"$1_models.py"
  echo "Component $1 created!!"
fi

ls
