
setlmis([]);
[delta_,ndec,delta_dec] = lmivar(1,[mm,1]);
A_0L=[zeros(mm,nn-mm) eye(mm)]*A_0;
Ad_0L=[zeros(mm,nn-mm) eye(mm)]*Ad_;
beta=(b_/alpha_)*BBd_(1:n,:)'*BBd_(1:n,1);
delta_1=100000; 
delta_2=.0001;

lmi1 = newlmi;
lmiterm([lmi1 1 1 0],-PP*delta_1^2/beta);
lmiterm([lmi1 1 2 0],A_0L');
lmiterm([lmi1 2 2 0],-eye(mm));
lmi12 = newlmi;
lmiterm([lmi12 1 1 0],-PP*delta_2^2/beta);
lmiterm([lmi12 1 2 0],Ad_0L');
lmiterm([lmi12 2 2 0],-eye(mm));


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
lmisys=getlmis;
options=[1, 100, -1,10,0];
[tmin,xfeas] = feasp(lmisys,options);
rho=BBd_(nn,:)+delta_1+delta_2
sam_time=0.0001;


