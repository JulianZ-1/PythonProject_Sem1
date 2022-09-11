import React from 'react';
import './App.css';
import InputField from './components/InputField';
import {useState} from 'react'
import { Todo } from './model';



// //In type script, you have to define all the varables like below
// let age: number;
// //below is the union format, which means you can assign both
// let name: string | number;
// let isStudent: boolean;
// //this is how to define a array
// let hobbies: string[];
// //this is how you define an array with only two require elemensts
// let role:[number, string];

// //like anytype
// let personName: unknown;

// //this is an interface question mark is options
// interface Person {
//   name: string
//   age?: number
// }

// //this is now you can extend interfaces in TS
// interface Guy extends Person {
//   profession: string
// }

// let x: Guy = {
//   name: "julian",
//   age: 24,
//   profession: "i dont know"  
// }



// type X = {
//   a: string
//   b: number
// }

//if you write it like this, when you create an Y, you need to also have the requirements from X
// type Y = X & {
//   c: string
//   d: number
// }



//never return undeviend, void return nothing
// let printName: (name: string) => never;


//this is how you can assign an interface
// let person: Person = {
//   name:"julian",
//   age: 24
// }

const App: React.FC = () =>{
  const [todo, setTodo] = useState<string>("")
  const [tpdp1, seTpdp1] = useState<Todo[]>([])

  const handleAdd = (e: React.FormEvent) => {
    e.preventDefault();
  }

  console.log(todo)
  return (
  <div className='App'>
    <span className='heading'>Taskify</span>
    <InputField todo = {todo} setTodo={setTodo} handleAdd = {handleAdd}>
  </div>
  );
}

export default App;
