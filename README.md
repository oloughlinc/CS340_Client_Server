# CS340_Journal

# How do you write programs that are maintainable, readable, and adaptable? Especially consider your work on the CRUD Python module from Project One, which you used to connect the dashboard widgets to the database in Project Two. What were the advantages of working in this way? How else could you use this CRUD Python module in the future?

Nobody wants to inherit and/or work on a messy monolithic source. Software development is hard enough already. That is why it is important for every developer to focus on maintainability, readability, and adaptability. 

This project displays adaptability by using three smaller, generalized pieces to create the whole. The data behind this project is stored itself on a MongoDB server (not included in this repo), the CRUD module is a standalone middleware to communicate easily with the mongo server (and can be easily purposed for a variety of CRUD operations), and the dashboard only lays out the display pieces and makes appropriate calls.

This also lends itself to maintainability. Since the project is broken into small pieces, work can be done on individual modules in the future without having to 'dig up' the whole project. Work is easier to scope and track.

Finally, readability should be a constant consideration when writing and refactoring your code. Appropriate comments are placed in this project that explain in words the layout and process of the code. Documentation is created to help understand the basic functions on an API level.

# How do you approach a problem as a computer scientist? Consider how you approached the database or dashboard requirements that Grazioso Salvare requested. How did your approach to this project differ from previous assignments in other courses? What techniques or strategies would you use in the future to create databases to meet other client requests?

The focus of this project was to use a client-server relationship through the use of a MVC pattern. The logic is stored seperately from the client display. As a computer scientist it is best to break a problem down into smaller pieces that are then simpler to work with, in a 'divide-and-conquer' manner. Here, we have divided the client's problem into three smaller parts and developed and tested them seperately. This becomes especially important with complex problems. It eases development and ensures a higer quality final product.

# What do computer scientists do, and why does it matter? How would your work on this type of project help a company, like Grazioso Salvare, to do their work better?

Computer scientists solve problems. It matters because the world is full of problems. What does this data mean? How can I reach customers? Can we make this process easier? Computers technology (along with many fields) is driven by these problems, and there will always be a need for problem solvers. The problem we have solved here for the client is allowing them to quickly analyze a large set of data in a simple and intuitive way. This is a great example of how computers and computer scientists can contribute to the world. 

