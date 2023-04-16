# Vacation Bucket List
## Resource
<p> Vacation</p>
<p> Attributes:</p>
<ul> 
<li> location (string)
<li> activity (string)
<li> climate (string)
<li> cost (string)
<li> length (string)
</ul>
<p> User</p>
<p> Attributes:</p>
<ul> 
<li> fname (string)
<li> lname (string)
<li> email (string)
<li> pass (string)
</ul>

## Schema

```CREATE TABLE vacations (id INTEGER PRIMARY KEY, location TEXT, activity TEXT, climate TEXT, cost TEXT, length TEXT); ```
***
```CREATE TABLE users (id INTEGER PRIMARY KEY, fname TEXT, lname TEXT, email TEXT, pass TEXT);```

## REST Endpoints

<table>
  <tr>
    <th>Name</th>
    <th>Method</th>
    <th>Path</th>
  </tr>
  <tr>
    <td>Retrieve vacation collection</td>
    <td>GET</td>
    <td>/vacations</td>
  </tr>
  <tr>
    <td>Retrieve vacation member</td>
    <td>GET</td>
    <td>/vacations/{id}</td>
  </tr>
    <tr>
    <td>Create vacation member</td>
    <td>POST</td>
    <td>/vacations</td>
  </tr>
    <tr>
    <td>Update vacation member</td>
    <td>PUT</td>
    <td>/vacations/{id}</td>
  </tr>
    <tr>
    <td>Delete vacation member</td>
    <td>DELETE</td>
    <td>/vacations/{id}</td>
    <tr>
    <td>Create user member</td>
    <td>POST</td>
    <td>/users</td>
  </tr>
    <tr>
    <td>Create session member</td>
    <td>POST</td>
    <td>/sessions</td>

</table>

## Password Hashing
<p>I implemented password hashing using bcrpyt with default settings.</p>

``` hash= bcrpyt.hash(password)```
