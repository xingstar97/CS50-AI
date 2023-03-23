from model import model

# Calculate predictions
predictions = model.predict_proba({
    "train": "delayed"
})

# Print predictions for each node
for node, prediction in zip(model.states, predictions):
# The zip() function returns a zip object, which is an iterator of tuples where the first item in each passed iterator is paired together, 
# and then the second item in each passed iterator are paired together etc.
    if isinstance(prediction, str):
        print(f"{node.name}: {prediction}")
    else:
        print(f"{node.name}")
        for value, probability in prediction.parameters[0].items():
            print(f"    {value}: {probability:.4f}")
