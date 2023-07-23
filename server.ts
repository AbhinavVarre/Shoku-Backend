import { Request, Response } from 'express';

const express = require('express')
const app = express()

app.get('/api', (req:Request,res:Response) => {
    res.json({"monkeys": ['bonobo', 'ape', 'chimpanzee']})
})

app.get('/', (req:Request,res:Response) => {
    res.send("Welcome to the shoku backend!!!")
})

app.listen( 5001, () => {console.log("server started")})