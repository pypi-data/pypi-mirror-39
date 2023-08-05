class TransformRef:
    id = None
    transform_path = None
    children = []
    parent = None

    def __init__(self, transform_path):
        self.id = id
        self.transform_path = transform_path

    def add_child_ref(self, transform_ref):
        """
        Adds the TransformRef if it is not already added.
        :param transform_ref:
        :return:
        """
        if not isinstance(transform_ref, TransformRef):
            raise ValueError("transform_ref must be of type TransformRef")

        for child in self.children:
            if child is transform_ref:
                return

        transform_ref.parent = self
        self.children.append(transform_ref)

    def create_child_ref(self, transform_path, child_id=None):
        """
        Creates a new child TransformRef with transform_path specified.
        :param transform_path:
        :param child_id:
        :return: TransformRef child
        """
        transform_ref = TransformRef(transform_path, child_id)
        self.add_child_ref(transform_ref)
        return transform_ref

    def get_rendered_transform_path(self):
        """
        Generates a rendered transform path
        that is calculated from all parents.
        :return:
        """
        path = self.transform_path
        parent = self.parent

        while parent is not None:
            path = "{0}/{1}".format(parent.transform_path, path)
            parent = parent.parent

        return path

    def get_rendered_transform_path_relative(self, relative_transform_ref):
        """
        Generates a rendered transform path relative to
        parent.
        :param relative_transform_ref:
        :return:
        """
        path = self.transform_path
        parent = self.parent

        while parent is not None and parent is not relative_transform_ref:
            path = "{0}/{1}".format(parent.transform_path, path)
            parent = parent.parent

        return path