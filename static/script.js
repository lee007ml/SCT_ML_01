document.getElementById("predictionForm").addEventListener("submit", async function (e) {
  e.preventDefault();

  const data = {
    GrLivArea: document.getElementById("GrLivArea").value,
    BedroomAbvGr: document.getElementById("BedroomAbvGr").value,
    FullBath: document.getElementById("FullBath").value,
    GarageArea: document.getElementById("GarageArea").value,
    YearBuilt: document.getElementById("YearBuilt").value,
    OverallQual: document.getElementById("OverallQual").value
  };

  const response = await fetch("/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });

  const result = await response.json();
  const resultDiv = document.getElementById("result");

  if (result.price) {
    resultDiv.innerHTML = `Estimated Price: ₹${result.price.toLocaleString()}`;
  } else {
    resultDiv.innerHTML = `Error: ${result.error}`;
  }
});
