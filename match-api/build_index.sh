# Log the start time and initial resource usage
echo "Script started at $(date)"
echo "Initial memory usage:"
free -h
echo "Initial disk usage:"
df -h

python -m index.store_load


# Log the end time and final resource usage
echo "Script ended at $(date)"
echo "Final memory usage:"
free -h
echo "Final disk usage:"
df -h