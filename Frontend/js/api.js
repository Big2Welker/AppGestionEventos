const API = "/api/v1";

function getToken() {
  return localStorage.getItem("token");
}

function authHeaders(withJson = false) {
  const headers = {};

  if (withJson) {
    headers["Content-Type"] = "application/json";
  }

  const token = getToken();
  if (token) {
    headers["Authorization"] = "Bearer " + token;
  }

  return headers;
}

function logout() {
  localStorage.clear();
  window.location.href = "index.html";
}