export function serverUrl(path) {
  if(window.location.hostname === 'localhost')
    return 'http://localhost:5000'+path

  return 'https://ghrmz7xo12.execute-api.us-east-1.amazonaws.com/prod'+path
}