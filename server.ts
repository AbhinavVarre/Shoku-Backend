import { Request, Response } from 'express';

//starter server file
const express = require('express')
const app = express()


app.get('/api', (req:Request,res:Response) => {
    res.json({"monkeys": ['bonobo', 'ape', 'chimpanzee']})
})

app.get('/', (req:Request,res:Response) => {
    res.send("Welcome to the shoku backend!!!")
})

//hi

app.listen( 5001, '127.0.0.1', () => {console.log("server started")})