#encoding "cp1251"

// ������ ���

// ��������
Initials -> Word<wff=/[�-�]\./> Word<wff=/[�-�]\./> | Word<wff=/([�-�]\.){1,2}/>;

// ��� � ��������
Name -> Word<kwtype="���", rt, gnc-agr[1]> Word<kwtype="��������", gnc-agr[1]>;
Name -> Word<kwtype="���", rt> Word<kwtype="��������"> { weight = 0.9 };
Name -> Word<kwtype="���", rt>;
Name -> Word<kwtype="���", rt, gnc-agr[1]> Word<gnc-agr[1]> { weight = 0.7 };
Name -> Word<h-reg1, rt, gnc-agr[1]> Word<h-reg1, gnc-agr[1]> { weight = 0.5 };
Name -> Word<h-reg1, rt> Word<h-reg1> { weight = 0.3 };
Name -> Word<h-reg1, rt> { weight = 0.3 };

// �������
Surname -> Word<kwtype="�������">;
Surname -> Word<wff=/���-[�-�].*/> { weight = 0.8 };
Surname -> '���' Word<h-reg1, rt> { weight = 0.8 };
Surname -> Word<h-reg1> { weight = 0.4 };

// ���
FullName -> Initials interp (+Occupation.Who) Surname<rt> interp (Occupation.Who) { weight = 0.8 };
FullName -> Surname<rt> interp (Occupation.Who) Initials interp (+Occupation.Who) { weight = 0.8 };

FullName -> Name<rt, gnc-agr[1]> interp (+Occupation.Who) Surname<gnc-agr[1]> interp (Occupation.Who);
FullName -> Name<rt> interp (+Occupation.Who) Surname interp (Occupation.Who) { weight = 0.9 };
FullName -> Surname<gnc-agr[1]> interp (Occupation.Who) Name<rt, gnc-agr[1]> interp (+Occupation.Who) { weight = 0.95 };
FullName -> Surname interp (Occupation.Who) Name<rt> interp (+Occupation.Who) { weight = 0.85 };

// ������������ ���������������
NounList -> Noun;
NounList -> NounList<rt, nc-agr[1]> ',' Noun<nc-agr[1]> | NounList<rt, nc-agr[1]> '�' Noun<nc-agr[1]>;

// ������� ������ ��� ������ ����������
NP -> Noun | Adj<gnc-agr[1]> NP<gnc-agr[1], rt> | NP<rt> NounList<gram="gen"> | NP<rt> '�' Noun<gram="ins">;

// ��������, ������������ �������������� ������������� ��� ��������
AcquisitivePrep -> '��' | '�' | '��';

// �������������
// '��' ������� � AcquisitivePrep, �� ������� �����, ����� ���� "�� ����...", �� �� "�� ������"
Division -> Adj<gnc-agr[1]> Noun<kwtype="local_division", rt, gnc-agr[1]> (Word<gram="gen", kwtype="employer_type">) |
	 (AcquisitivePrep) Noun<kwtype="struct_division", rt> NP<gram="gen"> (Word<gram="gen", kwtype="employer_type">);

// ��� ���������������-��������������� ������� ��� ������������
TerrName -> AnyWord<kwtype="terr", rt> AnyWord<h-reg1> AnyWord<kwtype="��"> |
	AnyWord<kwtype="terr", rt> AnyWord<kwtype="��"> AnyWord<h-reg1> |
	Noun<kwtype="state_division", rt> Word<kwtype="terr"> Word<kwtype="principality"> |
	(Adj<gnc-agr[1]>) Word<kwtype="terr", rt, gnc-agr[1]> Word<kwtype="principality"> |
	Word<kwtype="adj_principality", gnc-agr[1]> Word<kwtype="terr", rt, gnc-agr[1]>;

// ��-�� ������� �������� ���� ������ �������� ���������� Principality � ������ ����������� TerrName
TerrName -> Word<kwtype="principality"> { weight = 0.8 };
TerrName -> Word<kwtype="implicit_principality"> { weight = 0.1 };

// ��������������� �������������� (����. "������� ��� (�����������)")
Adjunct -> Adj<gnc-agr[1]> Word<kwtype="adjunct", rt, gnc-agr[1]>;
Adjunct -> Word<kwtype="adjunct", rt> '��' NP<gram="dat">;

// ��� ���������������-��������������� ������� ��� ��������������� ������� ��� �������
Principality -> AnyWord<kwtype="��", rt> AnyWord<h-reg1> | AnyWord<h-reg1> AnyWord<kwtype="��", rt> | Word<kwtype="principality">;

// ������� ��� ����������� ���������������� ����������� ���������� ���������
LocalPrep -> '��';

// ��������������� ����������� ���������� ���������
Locality -> LocalPrep Principality<rt, gram="dat">;

Locality -> Locality<rt, c-agr[1]> '�' Principality<c-agr[1]> | Locality<rt, c-agr[1]> ',' Principality<c-agr[1]>;


// ��������� ��� �����������

// �� ������� ������� ��������� ��� ���������� ����
OrgName -> Division<rt> NP<quoted> |
	Word<rt, kwtype="employer_type"> NP<quoted>;

// �� ��������� � �������� � �������� ��� � ������� �����
OrgName -> Division<rt> Word<h-reg1, quoted> { weight = 0.4 };
OrgName -> Division<rt> Word<h-reg1, l-quoted> Word<h-reg1, ~l-quoted, ~r-quoted>* Word<h-reg1, r-quoted> { weight = 0.3 };
OrgName -> Division<rt> Word<h-reg1, ~l-quoted, ~r-quoted>+ { weight = 0.2 };

// ���������������-��������������� �������
OrgName -> TerrName;

// ������������ ����������� (����. "�������� ������ ����������� ����������")
OrgName -> (Adj<gnc-agr[1]>) Word<kwtype="institution", rt, gnc-agr[1]> '��' NP<gram="dat"> |
	(Adj<gnc-agr[1]>) Word<kwtype="institution", rt, gnc-agr[1]> '��' NP<gram="acc"> |
	(Adj<gnc-agr[1]>) Word<kwtype="institution", rt, gnc-agr[1]> '������' NP<gram="abl"> |
	(Adj<gnc-agr[1]>) Word<kwtype="council", rt, gnc-agr[1]> NP<gram="gen"> Principality<gram="gen">;

// ��������� �����������
OrgName -> AnyWord<kwtype="known_org">;

// �������� ��������� ��� �������� ����������
OrgName -> Noun<kwtype="state_division", rt> AnyWord<kwtype="terr"> { weight = 0.4 };

// �������� ��������� ��� ���������
OrgName -> AnyWord<kwtype="terr"> { weight = 0.1 };

// ������������
OrgName -> Word<wff=/[�-�]+/> { weight = 0.7 };

// ����� � �������� (������ ������� ���������� ���������� ��������)
OrgName -> (Adj<gnc-agr[1]>) NP<quoted, rt, gnc-agr[1]> { weight = 0.6 };

// ������������������ ���� � ������� ����� ��� ������� �������� ����
OrgName -> Word<h-reg1> Word<h-reg1>+ { weight = 0.4 };

// ������� �� ���� ������ �������� �������� ��� �������� ����, ��� ��� ������ ������������ ��������, ������������ ��, � �� �������� �� �� ��������� ����������
// ������������� ��������������� ��������������
OrgName -> Adjunct '���' OrgName<gram="abl">;
// ������������� ���������������� �����������
OrgName -> OrgName Locality;

// ������ ����������� ��� ����������������� (����., "���������� ��� � ������")
// ��� ����������������� �� ���������� � ������������� �����������
Representation -> AcquisitivePrep Principality<rt>;
Representation -> '�' '������';
Representation -> Representation<rt, gnc-agr[1]> '�' Principality<gnc-agr[1]> |
	Representation<rt, gnc-agr[1]> ',' Principality<gnc-agr[1]>;

// ������������ ����������� ��� ������� ����� ������� ("���� X, Y � Z")
OrgList -> OrgName interp (Occupation.Where) (Representation);
OrgList -> OrgList<rt, c-agr[1]> ',' OrgName<c-agr[1]> interp (Occupation.Where) (Representation) |
	OrgList<rt, c-agr[1]> '�' OrgName<c-agr[1]> interp (Occupation.Where) (Representation);

// ���������
Position -> Noun<kwtype="position">;
Position -> Word<wff=/[��]��-.*/>;
Position -> Word<kwtype="sub_position", rt> Position<gram="gen">;

// ������ ��� ��������� ����� ������ � ���������
Job -> Word<kwtype="of_principality"> interp (Occupation.Where)
	Position<rt> interp (Occupation.Position);

Job -> Position<rt> interp (Occupation.Position)
	OrgList<gram="gen">;

Job -> Position<rt> interp (Occupation.Position)
	AcquisitivePrep
	OrgList<gram="gen"> { weight = 0.5 };

// ����������� ������� ��� ���������������� ��������������, ����. "����� ������ � ������"
// ���������� ����������� ������� � �������� ���� Position
Job -> Position<rt> interp (Occupation.Position)
	Principality<gram="gen"> interp (Occupation.Where)
	Representation interp (+Occupation.Position::norm="abl");

// ������ ���� ������, ������ �� ��� ����� ���
// �������� � ���� ������� ������ ������ ����, ����� ��������� ��������, ����� ������ �� �������� ������������ ������������ ������ (����. "��������� ������������� � [������]")
JobList -> Job<rt>;
JobListPre -> Job<rt>;
JobList -> JobList<rt, gnc-agr[1]> '�' Job<gnc-agr[1]> | JobList<rt, gnc-agr[1]> ',' Job<gnc-agr[1]>;
JobListPre -> JobListPre<rt, gnc-agr[1]> '�' Job<gnc-agr[1]> | JobListPre<rt, gnc-agr[1]> ',' Job<gnc-agr[1]> | JobListPre<rt, gnc-agr[1]> Job<gnc-agr[1]>;
JobList -> NP<rt> { weight = 0.3 };
JobList -> JobList<rt, gnc-agr[1]> '�' NP<gnc-agr[1]> { weight = 0.3 };
JobList -> JobList<rt, gnc-agr[1]> ',' NP<gnc-agr[1]> { weight = 0.3 };
JobListPre -> JobListPre<rt, gnc-agr[1]> '�' NP<gnc-agr[1]> { weight = 0.3 };
JobListPre -> JobListPre<rt, gnc-agr[1]> ',' NP<gnc-agr[1]> { weight = 0.3 };
JobListPre -> JobListPre<rt, gnc-agr[1]> NP<gnc-agr[1]> { weight = 0.3 };

// ���������� ������� ����
Occupation -> JobListPre
	FullName<rt>;

Occupation -> FullName<rt> ',' JobList '.' |
	FullName<rt> ',' JobList ',' |
	FullName<rt> ',' JobList EOSent;

Occupation -> FullName<rt> Hyphen JobList '.' |
	FullName<rt> Hyphen JobList ',' |
	FullName<rt> Hyphen JobList EOSent;

