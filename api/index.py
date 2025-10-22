import json

def handler(event, context):
    """Simple handler function for Vercel"""
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'message': 'API is working!',
            'status': 'ok',
            'test': True
        })
    }
