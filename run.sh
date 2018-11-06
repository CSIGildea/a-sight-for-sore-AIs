#!/bin/bash
activate () {
  . ../.env/bin/activate
}
python face_recognition_threaded.py
echo "Completed finding specificied individual - See result in answers.csv"
