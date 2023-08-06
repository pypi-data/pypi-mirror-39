class View:

  def setup(self, root_folder, outputs, parameters, force_start_index=None, force_end_index=None):
    '''Initializes the database'''

    return True


  def done(self):
    '''Should return ``True``, when data is finished'''

    return True


  def next(self):
    '''Loads the next data block on ``outputs``'''

    return True
