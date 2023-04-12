export function serverUrl(path) {
  if(window.location.hostname === 'localhost')
    return 'http://localhost:5000'+path

  return 'https://d9fr3dwx8e.execute-api.ca-central-1.amazonaws.com/prod'+path
}

export function getLocalUser(){
    let user_str = sessionStorage.getItem("user")
    if (user_str===undefined || user_str==="undefined") {
        return null
    }
    let user = JSON.parse(user_str)
    return user
}