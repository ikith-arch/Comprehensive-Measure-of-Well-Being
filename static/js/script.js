// HDI Prediction System

console.log("HDI Prediction System Loaded Successfully");

// Prevent negative numbers
document.addEventListener("DOMContentLoaded", function () {

    const inputs = document.querySelectorAll("input[type='number']");

    inputs.forEach(function(input){

        input.addEventListener("input", function(){

            if(this.value < 0){
                this.value = "";
            }

        });

    });

});