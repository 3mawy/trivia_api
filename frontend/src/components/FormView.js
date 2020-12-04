import React, { Component } from 'react';
import $ from 'jquery';

import '../stylesheets/FormView.css';

class FormView extends Component {
  constructor(props){
    super();
    this.state = {
      question: "",
      answer: "",
      difficulty: 1,
      category: 1,
      categories: {},
      errors: {
        question: "",
        answer: "",
        difficulty: "",
        category: "",
      }
    }
  }

  componentDidMount(){
    $.ajax({
      url: `/categories`, //TODO: update request URL
      type: "GET",
      success: (result) => {
        this.setState({ categories: result.categories.find(category => category.type) })
        return;
      },
      error: (error) => {
        alert('Unable to load categories. Please try your request again')
        return;
      }
    })
  }


  submitQuestion = (event) => {
    event.preventDefault();
    $.ajax({
      url: '/questions', //TODO: update request URL
      type: "POST",
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({
        question: this.state.question,
        answer: this.state.answer,
        difficulty: this.state.difficulty,
        category: this.state.category
      }),
      xhrFields: {
        withCredentials: true
      },
      crossDomain: true,
      success: (result) => {
        document.getElementById("add-question-form").reset();
        return;
      },
      error: (error) => {
        alert('Unable to add question. Please try your request again')
        return;
      }
    })
  }

  validateForm = (errors) => {
    let valid = true;
    Object.values(errors).forEach(
      // if we have an error string set valid to false
      (val) => val.length > 0 && (valid = false)
    );
    return valid;
  }

  handleChange = (event) => {
    event.preventDefault();
    const { name, value } = event.target;
    let errors = this.state.errors;

    switch (name) {
      case 'question':
        errors.question =
          value.length < 1
            ? 'empty question field is not valid!'
            : '';
        break;
        case 'answer':
          errors.answer =
            value.length < 1
              ? 'empty answer field is not valid!'
              : '';
        break;
        case 'difficulty':
          errors.difficulty =
            value.length < 1
              ? 'empty difficulty field is not valid!'
              : '';
        break;
        case 'category':
          errors.category =
            value.length < 1
              ? 'empty category field is not valid!'
              : '';
        break;
        default:
        break;
    }

    this.setState({errors, [name]: value}, ()=> {
        console.log(errors)

    })
        this.setState({[event.target.name]: event.target.value})

  }

  render() {
    const {errors} = this.state;
    return (
      <div id="add-form">
        <h2>Add a New Trivia Question</h2>
        <form className="form-view" id="add-question-form" onSubmit={this.submitQuestion}>
          <label>
            Question
            <input type="text" name="question" onChange={this.handleChange}/>
            <br/>{errors.question.length > 0 && <span style={{color: "red", fontSize: '10px'}} className='error'>{errors.question}</span>}
          </label>
          <label>
            Answer
            <input type="text" name="answer" onChange={this.handleChange}/>
            <br/>{errors.answer.length > 0 && <span style={{color: "red", fontSize: '10px'}} className='error'>{errors.answer}</span>}
          </label>
          <label>
            Difficulty
            <select name="difficulty" onChange={this.handleChange}>
              <option value="1">1</option>
              <option value="2">2</option>
              <option value="3">3</option>
              <option value="4">4</option>
              <option value="5">5</option>
            </select>
          </label>
          <label>
            Category
            <select name="category" onChange={this.handleChange}>
              {Object.keys(this.state.categories).map(id => {
                  return (
                    <option key={id} value={id}>{this.state.categories[id]}</option>
                  )
                })}
            </select>
          </label>
          <input type="submit" className="button" value="Submit" />
        </form>
      </div>
    );
  }
}

export default FormView;
