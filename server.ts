import { Request, Response } from 'express';
import { Pool } from 'pg';

//starter server file
const express = require('express')
const app = express()


const pool = new Pool({
    host     : "shoku-dev.c8iml9o89lxg.us-east-2.rds.amazonaws.com",
    user     : "postgres",
    password : "shokudevdb",
    database : "postgres",
    port     : 5432
});



app.get('/api', (req:Request,res:Response) => {
    res.json({"monkeys": ['bonobo', 'ape', 'chimpanzee']})
})

app.get('/', (req:Request,res:Response) => {
    res.send("Welcome to the shoku backend!!!")
})

app.get('/api/restaurants', async (req:Request,res:Response) => {
    const result = await pool.query('SELECT * FROM restaurant')
    res.send(result.rows)
})

app.get('/api/restaurants/best', async (req:Request,res:Response) => {
    const result = await pool.query('SELECT name, rating FROM restaurant ORDER BY rating DESC;')
    res.send(result.rows)
})

app.get('/api/restaurants/mostpopular', async (req:Request,res:Response) => {
    const result = await pool.query('SELECT MAX(review) FROM restaurant;')
    res.send(result.rows)
})


app.listen( 5001, '127.0.0.1', () => {console.log("server started")})