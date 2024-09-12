import json
import boto3
import uuid
import re

def lambda_handler(event, context):

    # Obtener el texto del cuerpo de la solicitud
    texto = json.loads(event['body'])['texto']

    
    # Crear un cliente de Bedrock Agent Runtime
    client = boto3.client('bedrock-agent-runtime', region_name='us-east-1')

    # Configurar los parámetros de la solicitud al modelo de Bedrock
    agent_id = 'AGENTID'  # Reemplaza con el ID de tu agente
    agent_alias_id = 'ALIASID'  # Reemplaza con el alias de tu agente
    session_id = str(uuid.uuid4())  # Generar un nuevo ID de sesión

    # Configurar la solicitud
    payload = {
        "inputText": texto,
        "enableTrace": False,  # Cambia a True si deseas habilitar el trazado
        "endSession": False  # Cambia a True si deseas finalizar la sesión
    }

    try:
        # Hacer la solicitud a Bedrock Agent Runtime
        response = client.invoke_agent(
            agentId=agent_id,
            agentAliasId=agent_alias_id,
            sessionId=session_id,
            inputText=payload["inputText"],
            enableTrace=payload["enableTrace"],
            endSession=payload["endSession"]
        )
        
        # Procesar la respuesta
        result_text = ""
        for event in response['completion']:
            if 'chunk' in event:
                # Procesar cada fragmento del flujo de eventos
                chunk = event['chunk']
                if 'bytes' in chunk:
                    result_text += chunk['bytes'].decode('utf-8')
        
        # Encontrar la posición de "result":
        start = result_text.find('"result":') + len('"result":')

        # Extraer la parte del texto después de "result":
        result_text2 = result_text[start:].strip()

        # Eliminar las comillas iniciales y finales si están presentes
        if result_text2.startswith('"') and result_text2.endswith('"'):
            result_text2 = result_text2[1:-1]

        # Eliminar las partes con % solo si la respuesta no está vacía
        if result_text2:
            result_text2 = re.sub(r'%\[\d+\]%', '', result_text2)

        # Eliminar las comillas y llaves adicionales
        result_text2 = result_text2.strip('}"')

    except Exception as e:
        result_text2 = f'Error: {str(e)}'

    return {
        'statusCode': 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",  # Permitir todos los orígenes; ajusta esto en producción
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"  # Métodos permitidos
        },
        'body': json.dumps(result_text2)
    }
