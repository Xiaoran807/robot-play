% BBd=[0 0 0]';
T1=[eye(nn-mm) zeros(nn-mm,mm);K*C eye(mm)];
A_=T1*AA1*inv(T1);
A_11=A_(1:nn-mm,1:nn-mm);
A_12=A_(1:nn-mm,nn-mm+1:nn);
A_21=A_(nn-mm+1:nn,1:nn-mm);
A_22=A_(nn-mm+1:nn,nn-mm+1:nn);
Ad_=T1*Adf*inv(T1);
Ad_11=Ad_(1:nn-mm,1:nn-mm);
Ad_12=Ad_(1:nn-mm,nn-mm+1:nn);
Ad_21=Ad_(nn-mm+1:nn,1:nn-mm);
Ad_22=Ad_(nn-mm+1:nn,nn-mm+1:nn);
B_=T1*BB1;
BBd_=T1*BBd;
B2=BB1(nn);





setlmis([]);
[PP1,ndec,PP1dec] = lmivar(1,[nn-mm,1]);
[PP2,ndec,PP2dec] = lmivar(1,[mm,1]);
[PP,ndec,PPdec] = lmivar(3,[PP1dec zeros(nn-mm,mm);zeros(mm,nn-mm) PP2dec]);
[L1,ndec,L1dec] = lmivar(2,[mm,pp-mm]);
[L2,ndec,L2dec] = lmivar(2,[mm,mm]);
[S1,ndec,S1dec] = lmivar(2,[nn-mm,nn-mm]);
[S2,ndec,S2dec] = lmivar(2,[nn-mm,mm]);
[S3,ndec,S3dec] = lmivar(2,[mm,nn-mm]);
[S4,ndec,S4dec] = lmivar(2,[mm,mm]);
[S_,ndec,S_dec] = lmivar(3,[S1dec 0*S2dec;0*S3dec S4dec]);
[E1,ndec,E1dec] = lmivar(2,[nn-mm,nn-mm]);
[E2,ndec,E2dec] = lmivar(2,[nn-mm,mm]);
[E3,ndec,E3dec] = lmivar(2,[mm,nn-mm]);
[E4,ndec,E4dec] = lmivar(2,[mm,mm]);
[E_,ndec,E_dec] = lmivar(3,[E1dec 0*E2dec;0*E3dec E4dec]);
[R1,ndec,R1dec] = lmivar(2,[nn-mm,nn-mm]);
R_= lmivar(3,[R1dec zeros(nn-mm,mm);zeros(mm,nn-mm) zeros(mm,mm)]);

% parameter settings
alpha_=2;
b_=20;
v_=1;

lmi1 = newlmi;
lmiterm([lmi1 1 1 PP1], 1,A_11,'s');
lmiterm([lmi1 1 1 PP1], 1,alpha_);
lmiterm([lmi1 1 1 S1], 1,1);
lmiterm([lmi1 1 1 E1], 1,1);
lmiterm([lmi1 1 1 R1], -1,exp(-alpha_*hmax));
lmiterm([lmi1 1 2 PP1], 1,A_12);
lmiterm([lmi1 1 2 PP2], A_21',1);
lmiterm([lmi1 1 2 -L1], -C',1);
lmiterm([lmi1 1 3 0], zeros(nn-mm,nn));
lmiterm([lmi1 1 4 PP1], 1,Ad_11);
lmiterm([lmi1 1 4 R1], 1,exp(-alpha_*hmax));
lmiterm([lmi1 1 5 PP1], 1,Ad_12);
lmiterm([lmi1 1 6 PP1], 1,BBd_(1:n,:));
lmiterm([lmi1 1 7 R1], hmax*A_11',1);
lmiterm([lmi1 2 2 PP2], 1,A_22,'s');
lmiterm([lmi1 2 2 L2], -1,1,'s');
lmiterm([lmi1 2 2 PP2], alpha_,1);
lmiterm([lmi1 2 2 S4], 1,1);
lmiterm([lmi1 2 2 E4], 1,1);
lmiterm([lmi1 2 3 0], zeros(mm,nn));
lmiterm([lmi1 2 4 PP2], 1,Ad_21);
lmiterm([lmi1 2 5 PP2], 1,Ad_22);
lmiterm([lmi1 2 6 0], zeros(mm));
lmiterm([lmi1 2 7 R1], hmax*A_12',1);
lmiterm([lmi1 3 3 E_],-exp(-alpha_*hmax), 1);
lmiterm([lmi1 3 3 R_],-exp(-alpha_*hmax), 1);
lmiterm([lmi1 3 4 R1],exp(-alpha_*hmax)*[eye(nn-mm);zeros(mm,nn-mm)], 1);
lmiterm([lmi1 3 5 0],zeros(nn,mm));
lmiterm([lmi1 3 6 0],zeros(nn,mm));
lmiterm([lmi1 3 7 0],zeros(nn,nn-mm));
lmiterm([lmi1 4 4 R1],-2*exp(-alpha_*hmax), 1);
lmiterm([lmi1 4 4 S1],-(1-d)*exp(-alpha_*hmax), 1);
lmiterm([lmi1 4 6 0],zeros(nn-mm,mm));
lmiterm([lmi1 4 7 R1],hmax*Ad_11', 1);
lmiterm([lmi1 5 5 S4],-(1-d)*exp(-alpha_*hmax), 1);
lmiterm([lmi1 5 6 0],zeros(mm,mm));
lmiterm([lmi1 5 7 R1],hmax*Ad_12', 1);
lmiterm([lmi1 6 6 0],-b_*BBd_(1:n,:)'*BBd_(1:n,:));
lmiterm([lmi1 6 7 R1],hmax*BBd_'*[eye(nn-mm);zeros(mm,nn-mm)],1);
lmiterm([lmi1 7 7 R1],-1,1);

lmi12 = newlmi;
lmiterm([lmi12 1 1 PP1], 1,-1);
lmi16 = newlmi;
lmiterm([lmi16 1 1 PP2], 1,-1);    
lmi13=newlmi;
lmiterm([lmi13 1 1 S_],1,-1);
lmi14=newlmi;
lmiterm([lmi14 1 1 R1],1,-1);
lmi15=newlmi;
lmiterm([lmi15 1 1 E_],1,-1);

lmisys=getlmis;
options=[1, 100, -1,10,0];
[tmin,xfeas] = feasp(lmisys,options);
PP1= dec2mat(lmisys,xfeas,PP1);
PP2= dec2mat(lmisys,xfeas,PP2);
PP= dec2mat(lmisys,xfeas,PP);
L1= dec2mat(lmisys,xfeas,L1);
L2= dec2mat(lmisys,xfeas,L2);
S_= dec2mat(lmisys,xfeas,S_);
E_= dec2mat(lmisys,xfeas,E_);
G1=inv(PP2)*L1;
G2=inv(PP2)*L2;
A_0=A_-[zeros(nn-mm) zeros(nn-mm,mm);zeros(mm,nn-mm) G2*v_];




TT=CC1(:,nn-pp+1:nn);
TT1=CC1*inv(T1);
Gr=[G1 G2];
G=Gr*inv(TT1(:,nn-pp+1:nn));
F=[K 1]*inv(TT)
eA=eig(A_0);
U=BigA-BigB*G*BigC;
% Closed-loop eigenvalues.
sg=eig(U)
%sf=eig([zeros(1,1) -p3;zeros(5,1) a]-[0;b(:,1)]*F*[1 zeros(1,5); zeros(3,1) c]);


