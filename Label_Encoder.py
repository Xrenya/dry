from save_load_pickle import load_obj, save_obj
from sklearn.preprocessing import LabelEncoder

def encoder_decoder(df, columns, filename, decoder=False, test=False):
  """Encode and decode dataframe using sklearn.preprocessing.LabelEncoder()
  
  Arguments:
    df -- dataframe
    columns -- categorical columns
    filename -- save file using "save_load_pickle.py"
    decoder -- inverse label transformation
    test -- fit-transfrom using saved file dictionary

  Returns:
    Transformed or Inversed dataframe
  """
  if decoder:
    try:
      classes_dict = load_obj(filename)
      for col in columns:
        label_encoder = LabelEncoder()
        label_encoder.classes_ = classes_dict[col]
        df[col] = label_encoder.inverse_transform(df[col])
    except FileNotFoundError: 
      print("File not found")
  else:
    if test:
      try:
        classes_dict = load_obj(filename)
        for col in columns:
          label_encoder = LabelEncoder()
          label_encoder.classes_ = classes_dict[col]
          df[col] = label_encoder.fit_transform(df[col].astype(str))
      except FileNotFoundError: 
        print("File not found")
    else:
      classes_dict = {}
      for col in columns:
        label_encoder = LabelEncoder()
        label_encoder.fit(df[col].astype(str))
        df[col] = label_encoder.fit_transform(df[col].astype(str))
        classes_dict.update({col: label_encoder.classes_})
      save_obj(classes_dict, filename)
