document.querySelector('form[name="signup-form"]')?.addEventListener('submit', async (e) => {
  e.preventDefault();

  const _this = document.querySelector('form[name="signup-form"]')
  const form = e.target
  const data = JSON.stringify({
    name: form.name.value,
    email: form.email.value,
    password: form.password.value,
  })
  const errorContainer = _this.querySelector('.error')

  console.log(data);

  try {
    const res = await fetch('/user/signup', {
      body: data,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    const json_res = await res.json()
    if (res.status == 200) {
      console.log(json_res)

      document.querySelector('.successful-register').classList.remove('hidden')
      document.querySelector('.register').classList.add('hidden')
      document.querySelector('.signin').classList.add('hidden')
      const ta = document.querySelector('#private-key')
      ta.innerText = json_res['private_key']
    } else {
      errorContainer.innerHTML = json_res?.error || json_res
      errorContainer.classList.remove('hidden')
    }
  } catch(err) {
    console.error(err)
    errorContainer.innerHTML = err
    errorContainer.classList.remove('hidden')
  }
})


document.querySelector('#continue-btn')?.addEventListener('click', (e) => {
  e.preventDefault();

  window.location.href = '/dashboard'
})

document.querySelector('form[name="signin-form"]')?.addEventListener('submit', async (e) => {
  e.preventDefault();

  const _this = document.querySelector('form[name="signin-form"]')
  const form = e.target
  const data = JSON.stringify({
    email: form.email.value,
    password: form.password.value,
  })
  const errorContainer = _this.querySelector('.error')

  try {
    const res = await fetch('/user/signin', {
      body: data,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    })

    if (res.status === 200) {
      document.location.href = '/dashboard'
    } else {
      const json_res = await res.json()
      errorContainer.innerHTML = json_res?.error || json_res
      errorContainer.classList.remove('hidden')
    }
  } catch(err) {
    console.error(err)
    errorContainer.innerHTML = err
    errorContainer.classList.remove('hidden')
  }
})

document.querySelector('form[name="donation-form"]')?.addEventListener('submit', async (e) => {
  e.preventDefault()

  const _this = document.querySelector('form[name="donation-form"]')
  const form = e.target
  const data = JSON.stringify({
    amount: form.amount.value,
    'private-key': form['private-key'].value,
  })
  const errorContainer = _this.querySelector('.error')
  const successContainer = _this.querySelector('.success')

  try {
    const res = await fetch('/user/donation', {
      body: data,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    const json_res = await res.json()

    if (res.status === 200) {
      successContainer.innerHTML = json_res?.info || json_res
      successContainer.classList.remove('hidden')
      errorContainer.classList.add('hidden')
    } else {
      errorContainer.innerHTML = json_res?.info || json_res
      errorContainer.classList.remove('hidden')
      successContainer.classList.add('hidden')
    }
  } catch(err) {
    console.error(err)
    errorContainer.innerHTML = err
    errorContainer.classList.remove('hidden')
  } finally {
    const res = await fetch('/user/balance')
    
    const json_res = await res.json()
    document.querySelector('#balance').innerHTML = json_res.balance
  }
})