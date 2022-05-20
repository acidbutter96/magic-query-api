def get_token(client, username:str, password:str)->dict:
    response = client.post("/auth",headers={
        "app-key":"xxlome",
        "Content-Type": "application/json"
        },
        json={
        "username":username,
        "password":password}
    )
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert "id" in data

    return data
