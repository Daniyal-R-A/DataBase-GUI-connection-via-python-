--1--
SELECT TOP 1 O.EmployeeID
From Orders O
Where YEAR(O.OrderDate) = 1998

--2--
SELECT E.EmployeeID
From Employees E 
where E.ReportsTo in
(SELECT E.EmployeeID 
from Employees E
where E.ReportsTo is NULL)

--3--
Select DISTINCT ET.EmployeeID
From EmployeeTerritories ET
where ET.TerritoryID in
(Select T.TerritoryID
From Territories T
Inner Join Region R on R.RegionID = T.RegionID
where R.RegionDescription = 'Western' OR R.RegionDescription = 'Eastern')

--4--
Select C.ContactName
From Customers C
where C.Country = 'Germany'
UNION 
Select S.ContactName
From Suppliers S
where S.Country = 'Germany'


--5--
Select TOP 1 ProductName
From Products
where ProductID in
(Select Top 3 p.ProductID
from Products p
Order by p.UnitPrice DESC)
Order By ProductID 

--6--
Select EmployeeID,
Case
	When YEAR(GETDATE()) - YEAR(HireDate) > 5 Then 3
	When YEAR(GETDATE()) - YEAR(HireDate) between 3 and 5 Then 2
	Else 1
End as SeniorityLevel
From Employees

--7--
Select ProductName,
Case
	When UnitPrice > 80 Then 'Costly'
	When UnitPrice between 30 and 80 Then 'Economical'
	Else 'Cheap'
End as 'Types'
From Products
Order by 'Types'

--8--
Select ProductName,
Case
	When num_orders >= 50 Then 'Customer favourite'
	When num_orders between 30 and 49 Then 'Trending'
	When num_orders between 10 and 29 Then 'on the rise'
	Else 'not popular'
End as 'Trend'
From Products P
Inner Join 
(Select OD.ProductID, count(OD.OrderID) as 'num_orders'
from [Order Details] OD
where OD.OrderID in(
Select O.OrderID
from Orders O
where YEAR(OrderDate) = 1997)
Group By OD.ProductID) as T on T.ProductID = P.ProductID


--9--
Select C.CustomerID, ISNULL(T.OrderCount, 0) as 'Order Count'
from Customers C
Left Join 
(Select O.CustomerID, count(O.OrderID) as "OrderCount"
From Orders O
Group By (O.CustomerID)) T on T.CustomerID = C.CustomerID


--10--
Select Distinct O.CustomerID
From Orders O
where O.OrderID in
(Select OD.OrderID
from [Order Details] OD
where Od.UnitPrice > (Select AVG(P.UnitPrice) from Products P))

--11--
Select C.ContactName
From Customers C
where C.CustomerID in
(Select O.CustomerID
From Orders O
where O.OrderID in
(Select OD.OrderID
From [Order Details] OD
where OD.ProductID in 
(Select P.ProductID
From Products P
where P.CategoryID in
(Select CategoryID from Products
where ProductName = 'Chai'))))
Order By C.ContactName

--12--
Select C.ContactName, T.NumberOfOrders
From Customers C
Right Join
(Select Top 1 O.CustomerID, Count(O.OrderID) as 'NumberOfOrders'
From Orders O
Group By O.CustomerID
Order By 'NumberOfOrders' Desc) T on T.CustomerID = C.CustomerID

--13--
Select C.ContactName
From Customers C
where C.CustomerID in
(Select O.CustomerID
from Orders O
where O.OrderID in 
(Select OD.OrderID
from [Order Details] OD 
where OD.unitprice in
(Select Max(P.UnitPrice)
from Products p)))

--14--
Select AVG(T.Count) as 'AverageProductsPerOrder'
From (Select OD.OrderID, Count(OD.ProductID) as 'Count'
From [Order Details] OD
Group By (OD.OrderID)) T

--15--
Select C.CategoryName
from Categories C
where C.CategoryID in
(Select P.CategoryID
from Products P 
Group By P.CategoryID
Having AVG(P.UnitPrice) > (Select AVG(P.UnitPrice) From Products P))

--16--
Select Top 1 T.ProductName, T.UnitPrice
From (Select Top 2 P.ProductName, P.UnitPrice
From Products P
Order By P.UnitPrice Desc) T
Order By T.UnitPrice

--17-- 
Select (AVG(OD.UnitPrice* OD.Quantity)) as 'AverageOrderAmount'
from [Order Details] OD
where OD.OrderID in
(Select O.OrderID
From Orders O
where O.CustomerID in 
(Select C.CustomerID
From Customers C 
where C.Country = 'France')) 