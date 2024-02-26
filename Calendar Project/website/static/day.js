function addIngredientForm() {
    // Create a new div for the ingredient form
    var div = document.createElement('div');
    div.className = 'ingredient-form';

    // Add form fields
    div.innerHTML = `
        <h5>Ingredient</h5>
        <div class="mb-3">
            <label>Name</label>
            <input type="text" class="form-control" name="ingredientName[]">
        </div>
        <div class="mb-3">
            <label>Calories</label>
            <input type="number" class="form-control" name="ingredientCalories[]">
        </div>
        <!-- Add more fields for carbs, protein, fats as needed -->
    `;

    // Append this new div to the ingredientsSection
    document.getElementById('ingredientsSection').appendChild(div);
}
