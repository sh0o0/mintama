export const backgroundStyle = {
  data() {
    return {
      topStyle: {
        backgroundImage: 'url(/static/mintama/img/mintama-top.png)',
        backgroundPosition: 'center center',
        backgroundRepeat: 'no-repeat',
        backgroundAttachment: 'fixed',
        backgroundSize: '100% 100%',
        backgroundColor: '#464646',
      }
    }
  }
}

export const oauthBtns = {
  data() {
    return {
      oauthBtns: [
        {name:'twitter', href: '/socials/login/twitter'},
        {name:'google', href: '/socials/login/google-oauth2/'},
        {name:'github', href: '/socials/login/github/'},
      ]
    }
  }
}
