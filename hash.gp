{StringToDecimal(S) =
local(T, V, i, j, tmp);
T = "";
V = [];
for(i = 1, length(S),
    for(j = 32, 127,
        U = Strchr(j);
        tmp = concat(T, U);
        if(S < tmp, 
            V = concat(V, j - 1);
            T = concat(T, Strchr(j - 1)); 
            break)
        )
    );
	print(V);
return(subst(Pol(V),x,128))}

generateHashFunc(t, p, alpha, beta) = {
	return((s) ->
		d = StringToDecimal(s);
		print("D: ",d);
		n1 = d \ 2^(t-1);
		n2 = d % 2^(t-1);
		print("N1: ", n1);
		print("N2: ", n2);
		a = Mod(alpha, p) ^ n1;
		b = Mod(beta, p) ^ n2;
		print(a," ",b);
		r = lift(a * b);
		return(r);
	);
};

t = 56
p = 47687490304404143
alpha = 8691170756970600
beta = 36184489036644108
hash = generateHashFunc(t,p,alpha,beta)

\\t = 32
\\p = 2180082167
\\alpha = 485539736
\\beta = 329746418
\\hash = generateHashFunc(t,p,alpha,beta)

\\print(StringToDecimal("Test"));
\\print(StringToDecimal("Test2"));
\\print(StringToDecimal("Test3"));

\\print(hash("Test"))
\\print(hash("Bob"))
print(hash("whistler"));
\\print(hash("snake"));
\\s = "0..UQr3" 
\\print(hash(s))

