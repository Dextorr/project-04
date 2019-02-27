import React from 'react'
import ReactDOM from 'react-dom'
import { BrowserRouter, Route, Switch } from 'react-router-dom'
// import { Redirect } from 'react-router'
import axios from 'axios'
// import Tone from 'tone'
import Header from './components/common/Header'
import Home from './components/Home'
import Register from './components/Register'
import Login from './components/Login'


import Jam from './components/Jam'

import './scss/style.scss'

class App extends React.Component {
  constructor(){
    super()

    this.state= {

    }
  }
  componentDidMount(){
    axios.get('/api/users/1')
      .then(res =>{
        console.log(res.data)
        this.setState({user: res.data})
      } )
  }

  render(){
    if(!this.state.user) return null
    const jams = this.state.user.created_jams
    const currentJam = jams[jams.length-1]

    const JamWithProps = () => {
      return (
        <Jam {...currentJam}/>
      )
    }

    return(
      <BrowserRouter>
        <main>
          <Header />
          <Switch>
            <Route path="/register" component={Register} />
            <Route path="/login" component={Login} />
            <Route path="/jam" component={JamWithProps} />
            <Route path="/" component={Home} />
          </Switch>
        </main>
      </BrowserRouter>
    )
  }
}

ReactDOM.render(
  <App />,
  document.getElementById('root')
)
