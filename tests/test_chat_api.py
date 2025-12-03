import json
import pytest
import azure.functions as func
from function_app import chat_api, health_check


class TestChatAPI:
    """Test cases for the Chat API endpoint"""
    
    def test_chat_api_success(self):
        """Test successful chat API request"""
        # Arrange
        req = func.HttpRequest(
            method='POST',
            url='/api/chat',
            body=json.dumps({
                'message': 'Hello, Azure!',
                'user_id': 'test_user_123'
            }).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        
        # Act
        response = chat_api(req)
        
        # Assert
        assert response.status_code == 200
        response_data = json.loads(response.get_body().decode('utf-8'))
        assert response_data['status'] == 'success'
        assert response_data['user_id'] == 'test_user_123'
        assert response_data['message_received'] == 'Hello, Azure!'
        assert 'Echo: Hello, Azure!' in response_data['response']
        assert 'timestamp' in response_data
    
    def test_chat_api_empty_message(self):
        """Test chat API with empty message"""
        # Arrange
        req = func.HttpRequest(
            method='POST',
            url='/api/chat',
            body=json.dumps({
                'message': '',
                'user_id': 'test_user_123'
            }).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        
        # Act
        response = chat_api(req)
        
        # Assert
        assert response.status_code == 400
        response_data = json.loads(response.get_body().decode('utf-8'))
        assert 'error' in response_data
        assert 'required' in response_data['error'].lower()
    
    def test_chat_api_missing_message_field(self):
        """Test chat API without message field"""
        # Arrange
        req = func.HttpRequest(
            method='POST',
            url='/api/chat',
            body=json.dumps({
                'user_id': 'test_user_123'
            }).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        
        # Act
        response = chat_api(req)
        
        # Assert
        assert response.status_code == 400
        response_data = json.loads(response.get_body().decode('utf-8'))
        assert 'error' in response_data
    
    def test_chat_api_invalid_json(self):
        """Test chat API with invalid JSON"""
        # Arrange
        req = func.HttpRequest(
            method='POST',
            url='/api/chat',
            body=b'invalid json{',
            headers={'Content-Type': 'application/json'}
        )
        
        # Act
        response = chat_api(req)
        
        # Assert
        assert response.status_code == 400
        response_data = json.loads(response.get_body().decode('utf-8'))
        assert 'error' in response_data
        assert 'json' in response_data['error'].lower()
    
    def test_chat_api_anonymous_user(self):
        """Test chat API with anonymous user"""
        # Arrange
        req = func.HttpRequest(
            method='POST',
            url='/api/chat',
            body=json.dumps({
                'message': 'Hello from anonymous'
            }).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        
        # Act
        response = chat_api(req)
        
        # Assert
        assert response.status_code == 200
        response_data = json.loads(response.get_body().decode('utf-8'))
        assert response_data['status'] == 'success'
        assert response_data['user_id'] == 'anonymous'


class TestHealthCheck:
    """Test cases for the health check endpoint"""
    
    def test_health_check(self):
        """Test health check endpoint"""
        # Arrange
        req = func.HttpRequest(
            method='GET',
            url='/api/health',
            body=None
        )
        
        # Act
        response = health_check(req)
        
        # Assert
        assert response.status_code == 200
        response_data = json.loads(response.get_body().decode('utf-8'))
        assert response_data['status'] == 'healthy'
        assert 'timestamp' in response_data


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
