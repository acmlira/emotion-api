from flask import Flask, request, jsonify
from transformers import pipeline
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

# Load the model
classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    top_k=None
)

@app.route("/v1/analysis", methods=["POST"])
def analyze():
    """
    Emotion Analysis
    ---
    post:
      summary: Detect the predominant emotion in a given text
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                text:
                  type: string
                  example: I'm very upset with this app
      responses:
        200:
          description: Detected emotion successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  emotion:
                    type: string
                    example: anger
                  score:
                    type: number
                    example: 0.9876
                  full_result:
                    type: array
                    items:
                      type: object
                      properties:
                        label:
                          type: string
                          example: sadness
                        score:
                          type: number
                          example: 0.5432
        400:
          description: Invalid request
    """
    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "The 'text' field is required"}), 400

    text = data["text"]
    result = classifier(text)
    sorted_result = sorted(result[0], key=lambda x: x["score"], reverse=True)
    top = sorted_result[0]

    return jsonify({
        "emotion": top["label"],
        "score": round(top["score"], 4),
        "full_result": sorted_result
    })

if __name__ == "__main__":
    app.run(debug=True)
