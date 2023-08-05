"""
Utility to create objects.
"""
from .action import Action


class Create(Action):
    """
    Utility to create objects.
    """
    def __init__(self, itop, class_name, **kwargs):
        super().__init__(itop, class_name, **kwargs)

    def create(self):
        """
        Execute the creation.
        :return: None
        """
        try:
            response = self.itop.create(self.class_name, **self.fields)
            if response['code'] == 0 and response['message'] is None:
                print("Created object {}".format(list(response['objects'].keys())[0]))
            else:
                raise RuntimeError("Error creating {class_name} : {message}".format(class_name=self.class_name,
                                                                                    message=response['message']))
        except IOError as exception:
            raise RuntimeError(str(exception))


def create(itop, class_name, **kwargs):
    """
    Creates an object.
    :param itop:  itop connection
    :param class_name: class of the object to create
    :param fields: content of the object
    :return:
    """
    Create(itop, class_name, **kwargs).create()
