%clear all
u0=0;
ac=-1;
dc=1;
a11=-70/3085;
a12=-2642.7/3085*u0;
Y_v_bar=-992/3085;
b1=1/3085;
a21=-442.2/915.5*u0;
a22=-105/915.5;
N_r_bar=-523.27/915.5;
b2=1/915.5;


% BigA=[-1 -1 -1;0 0 1;0 0 a11];
% BigAd=[0 0 0;0 0 0;0 0 0];
% BigB=[0 0 b1]';
% BigC=[0 1 0;0 0 1];
% Bdp=[0 0 0]';

% BigA=[-1 -1 -1;0 0 1;0 0 0];
% BigAd=[0 0 0;0 0 0;0 0 0];
% BigB=[0 0 1]';
% BigC=[1 0 0;0 0 1];
% Bdp=[1 0 0]'

ac=-1;
dc=1;
BigA=[ac dc 0 0;0 -1 -1 -1;0 0 0 1;0 0 0 a11];

BigAd=0*eye(4);
BigB=[0 0 0 b1]';
BigC=[0 1 0 0;0 0 1 0;0 0 0 1];
Bdp=[0 1 0 1]'


AA=BigA;
AAd=BigAd;
BB=BigB;
CC=BigC;
[nn,mm]=size(BB);
[pp,nn]=size(CC);
[nn,qq]=size(Bdp);
[AA11,BB11,CC11,Tcan,r]=outfor(BigA,BigB,BigC);
B2=BB11(nn-mm+1:nn,:);
Tt=[eye(nn-mm) zeros(nn-mm,mm);zeros(mm,nn-mm) inv(B2)];
AA1=Tt*AA11*inv(Tt);
BB1=Tt*BB11;
CC1=CC11*inv(Tt);
A=AA1(1:nn-mm,1:nn-mm);
B=AA1(1:nn-mm,nn);
C=[zeros(pp-mm,nn-pp) eye(pp-mm)];
[n,m] = size(B);
[p,n] = size(C);
Adf=Tt*Tcan*AAd*inv(Tcan)*inv(Tt);
Ad=Adf(1:nn-mm,1:nn-mm);
Bd=Adf(1:nn-mm,nn);
BBd=Tt*Tcan*Bdp;
%Bumm=BBd(1:n,:);
%Bum1=norm(Bumm(1,:));
% Bum2=norm(Bumm(2,:));
% Bum3=norm(Bumm(3,:));
% Bum4=norm(Bumm(4,:));
% Bum5=norm(Bumm(5,:));
% Bum=[Bum1 Bum2 Bum3 Bum4 Bum5]';
Bum=BBd(1:nn-mm,:);
Bm=BBd(nn-mm+1:nn,:);
%BBd=[Bum;Bm];


alpha=1.99;
bbb=.001;
delta=50;
epsilon=.01;
M=[30 1]';%M is some (pp-mm)*(nn-pp)matrix
hmax=0;
d=0;




setlmis([]);
[Q11,ndec,Q11dec] = lmivar(2,[n-p,n-p]);  
[Q12,ndec,Q12dec] = lmivar(2,[n-p,p]);
[Q22,ndec,Q22dec] = lmivar(2,[p,p]);
aQ = lmivar(3,[Q11dec  Q12dec;zeros(p,n-p) zeros(p,p)]);
bQ=lmivar(3,[zeros(n-p,p);Q22dec]);
cQ=lmivar(3,[zeros(n-p,n-p) zeros(n-p,p);zeros(p,n-p) Q22dec]);
[P,ndec,Pdec] = lmivar(1,[n,1]);
[Y,ndec,Ydec] = lmivar(2,[m,p]);
[S,ndec,Sdec]=lmivar(2,[nn-mm,nn-mm]);
[R,ndec,Rdec]=lmivar(2,[nn-mm,nn-mm]);
[E,ndec,Edec]=lmivar(2,[nn-mm,nn-mm]);
lmi1 = newlmi;
      lmiterm([lmi1 1 1 aQ], A,1,'s');
      lmiterm([lmi1 1 1 bQ], A,M*[eye(n-p) zeros(n-p,p)],'s');
      lmiterm([lmi1 1 1 cQ], A,delta,'s');
      lmiterm([lmi1 1 1 Y],-B,[eye(p)*M  delta*eye(p)] ,'s');
      
      
      
      
      lmiterm([lmi1 1 1 S],1,1);
      lmiterm([lmi1 1 1 P],alpha,1);
      lmiterm([lmi1 1 1 R],-exp(-alpha*hmax),1);
      lmiterm([lmi1 1 1 E],1,1);
      lmiterm([lmi1 1 2 P], 1,1);
      lmiterm([lmi1 1 2 aQ], 1,-1);
      lmiterm([lmi1 1 2 bQ], 1,-M*[eye(n-p) zeros(n-p,p)]);
      lmiterm([lmi1 1 2 cQ], 1,-delta);
      lmiterm([lmi1 1 2 -aQ], epsilon,A');
      lmiterm([lmi1 1 2 -bQ], epsilon*[eye(n-p) zeros(n-p,p)]'*M',A');
      lmiterm([lmi1 1 2 -cQ], epsilon,A'*delta);
      lmiterm([lmi1 1 2 -Y], -epsilon*[M'*eye(p); delta*eye(p)],B');
      lmiterm([lmi1 1 3 0],0);
      lmiterm([lmi1 1 4 aQ],Ad,1);
      lmiterm([lmi1 1 4 bQ], Ad,M*[eye(n-p) zeros(n-p,p)]);
      lmiterm([lmi1 1 4 cQ], Ad,delta);
      lmiterm([lmi1 1 4 Y],-Bd,[eye(p)*M  delta*eye(p)] );
      lmiterm([lmi1 1 4 R],exp(-alpha*hmax),1);
      lmiterm([lmi1 1 5 0],Bum);
      lmiterm([lmi1 2 2 aQ], -1, epsilon,'s');
      lmiterm([lmi1 2 2 bQ],  -epsilon,M*[eye(n-p) zeros(n-p,p)],'s');
      lmiterm([lmi1 2 2 cQ], -1, epsilon*delta,'s');
      lmiterm([lmi1 2 2 R],hmax^2,1);
      lmiterm([lmi1 2 3 0],0);
      lmiterm([lmi1 2 4 aQ], epsilon*Ad,1);
      lmiterm([lmi1 2 4 bQ], epsilon*Ad,M*[eye(n-p) zeros(n-p,p)]);
      lmiterm([lmi1 2 4 cQ], epsilon*Ad,delta);
      lmiterm([lmi1 2 4 Y],-epsilon*Bd,[eye(p)*M  delta*eye(p)]);
      lmiterm([lmi1 2 5 0],epsilon*Bum);
      lmiterm([lmi1 3 3 E],-exp(-alpha*hmax),1);
      lmiterm([lmi1 3 3 R],-exp(-alpha*hmax),1);
      lmiterm([lmi1 3 4 R],exp(-alpha*hmax),1);
      lmiterm([lmi1 3 5 0],0);
      lmiterm([lmi1 4 4 R],-2*exp(-alpha*hmax),1);
      lmiterm([lmi1 4 4 S],-(1-d)*exp(-alpha*hmax),1);
      lmiterm([lmi1 4 5 0],0);
      lmiterm([lmi1 5 5 0],-bbb*Bum'*Bum);

      lmi12 = newlmi;
      lmiterm([lmi12 1 1 P],1,-1);
      lmi13=newlmi;
      lmiterm([lmi13 1 1 S],1,-1);
      lmi14=newlmi;
      lmiterm([lmi14 1 1 R],1,-1);
      lmi15=newlmi;
      lmiterm([lmi15 1 1 E],1,-1);
      
%       lmi16 = newlmi;
%       lmiterm([lmi16 1 1 aQ],-1,1);
%       lmiterm([lmi16 1 1 bQ],-1,M*[eye(n-p) zeros(n-p,p)]);
%       lmiterm([lmi16 1 1 cQ],-1,delta);

      
lmisys=getlmis;
options=[1, 100, -1,10,0];
[tmin,xfeas] = feasp(lmisys,options);
P = dec2mat(lmisys,xfeas,P);
aQ = dec2mat(lmisys,xfeas,aQ);
bQ = dec2mat(lmisys,xfeas,bQ);
cQ = dec2mat(lmisys,xfeas,cQ);
Y= dec2mat(lmisys,xfeas,Y);
Q22=cQ(n-p+1:n,n-p+1:n);
Q2=aQ+delta*cQ+[zeros(nn-pp) zeros(nn-pp,pp-mm);Q22*M zeros(pp-mm)];
P_=inv(Q2)'*P*inv(Q2);
K=Y*inv(Q22)     


A_sum=A-B*K*C;
EG=eig(A_sum)
















