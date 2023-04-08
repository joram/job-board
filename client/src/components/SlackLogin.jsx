/* eslint-disable no-restricted-globals */

export default function SlackLogin ({
  slackClientId,
  slackUserScope = 'openid profile',
  redirectUrl,
}) {
  function handleClick () {
    let url = `https://slack.com/openid/connect/authorize?response_type=code&scope=${slackUserScope}&client_id=${slackClientId}`
    if (redirectUrl) { url += `&redirect_uri=${redirectUrl}` }
    location.href = url;
  }

  return (
    <a className='react-slack-login-a' style={{ cursor: 'pointer' }}>
      <img
        className='react-slack-login-img'
        onClick={handleClick}
        alt='Sign in with Slack'
        height='40'
        width='172'
        src='https://platform.slack-edge.com/img/sign_in_with_slack.png'
        srcSet='https://platform.slack-edge.com/img/sign_in_with_slack.png 1x, https://platform.slack-edge.com/img/sign_in_with_slack@2x.png 2x'
      />
    </a>
  )
}