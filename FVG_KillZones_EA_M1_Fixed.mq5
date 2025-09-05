// Corrected line 454 in the ResetDailyProfit function
// Change StringToString to StringToTime and remove the extra closing parenthesis

void ResetDailyProfit() {
    // ... previous code ...
    datetime time = StringToTime("2023.10.01 00:00"); // Corrected line
    // ... following code ...
}