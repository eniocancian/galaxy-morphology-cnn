import os
import argparse
import numpy as np
from tensorflow import keras
from tensorflow.keras.preprocessing.image import load_img, img_to_array

# Mapeamento oficial das 4 classes morfológicas
CLASS_NAMES = [
    'Elíptica',
    'Espiral',
    'Disco de Borda',
    'Irregular/Fusão'
]

def load_galaxy_model(model_path: str = None) -> keras.Model:
    """Carrega o modelo Keras salvo."""
    if model_path is None:
        base_dir = r'C:\Users\sueli\galaxy_zoo'
        model_path = os.path.join(base_dir, 'models', 'best_galaxy_cnn.keras')
        
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Modelo não encontrado em: {model_path}")
        
    return keras.models.load_model(model_path)

def preprocess_image(image_path: str, target_size=(128, 128)) -> np.ndarray:
    """Carrega e normaliza a imagem para inferência na CNN."""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Imagem não encontrada em: {image_path}")
        
    img = load_img(image_path, target_size=target_size)
    img_array = img_to_array(img)
    img_array = img_array / 255.0  # Normalização para [0, 1]
    return np.expand_dims(img_array, axis=0)  # Shape: (1, 128, 128, 3)

def predict_morphology(image_path: str, model_path: str = None):
    """Executa a inferência e exibe a distribuição de probabilidades."""
    print(f"\nCarregando modelo e analisando a imagem: {os.path.basename(image_path)}...")
    model = load_galaxy_model(model_path)
    img_tensor = preprocess_image(image_path)
    
    probabilities = model.predict(img_tensor, verbose=0)[0]
    predicted_idx = int(np.argmax(probabilities))
    predicted_label = CLASS_NAMES[predicted_idx]
    confidence = probabilities[predicted_idx] * 100
    
    print("\n" + "=" * 50)
    print(f"PREDIÇÃO MORFOLÓGICA: {predicted_label.upper()}")
    print(f"Grau de Confiança: {confidence:.2f}%")
    print("=" * 50)
    print("Distribuição de Probabilidades:")
    for label, prob in zip(CLASS_NAMES, probabilities):
        bar = "█" * int(prob * 30)
        print(f"  {label:<16} | {bar:<30} {prob * 100:6.2f}%")
    print("=" * 50 + "\n")
    
    return predicted_label, probabilities

if __name__ == "__main__":
    # Localizar automaticamente uma imagem válida existente na pasta
    img_dir = r'C:\Users\sueli\galaxy_zoo\galaxy-zoo-the-galaxy-challenge\images_training_rev1\images_training_rev1'
    
    default_img = None
    if os.path.exists(img_dir):
        available_images = [f for f in os.listdir(img_dir) if f.endswith('.jpg')]
        if available_images:
            default_img = os.path.join(img_dir, available_images[0])
            
    parser = argparse.ArgumentParser(description="Classificador Morfológico de Galáxias - Galaxy Zoo CNN")
    parser.add_argument("--image", type=str, default=default_img, help="Caminho para o arquivo da imagem .jpg")
    parser.add_argument("--model", type=str, default=None, help="Caminho opcional para o arquivo .keras do modelo")
    
    args, _ = parser.parse_known_args()
    
    if args.image is None or not os.path.exists(args.image):
        print(f"Nenhuma imagem encontrada automaticamente em: {img_dir}")
    else:
        predict_morphology(args.image, args.model)