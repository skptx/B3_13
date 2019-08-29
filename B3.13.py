import sys

class Tag:
    def __init__(self, tag, is_single = False, text = "", klass=None, **kwargs):
        self.is_single = is_single
        self.tag = tag
        self.text = text
        self.attributes = {}
        self.child = []
        if klass is not None:
            self.attributes["class"] = " ".join(klass)

        for attr, value in kwargs.items():
            if "_" in attr:
                attr = attr.replace("_", "-")
            self.attributes[attr] = value

    def __iadd__(self, other):
        self.child.append(other)
        return self

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        return self
    # Единая функция преоброзования тега в строку
    def __str__(self):
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append('%s="%s"' % (attribute, value))
        attrs = " ".join(attrs)
        if len(attrs)>0:
            attrs = " "+attrs

        if (self.is_single):
            return "<{tag}{attrs}/>\n".format(tag=self.tag, attrs=attrs)
        else:
            begin = "<{tag}{attrs}>{text}".format(tag=self.tag, attrs=attrs, text=self.text)
            childs = ""
            for curchild in self.child:
                childs = childs + str(curchild)
            if len(childs)>0:
                childs =("\n"+childs).replace("\n","\n ").rstrip()+"\n"
            
            end = "</{tag}>\n".format(tag=self.tag)
            return begin+childs+end



 
class HTML(Tag):
    def __init__(self, typeout, fileName = ""):
        self.typeout = typeout
        self.fileName = fileName
        super().__init__(tag="html")
    # Функция вывода кода ХТМД
    def outHTML(self):
        result = str(self)
        if self.typeout == "screen":
            print(result)
        if self.typeout == "file":
            with open(self.fileName, 'w') as f: 
                f.write(result)
   



class TopLevelTag(Tag):
    def __init__(self, tag):
        super().__init__(tag=tag)


if __name__ == "__main__":
    # Возмно передать 2 параметра, тип вывода (по умолчанию на экран) и имя файла для сохранения
    i = 0
    typeout="screen"
    filename="index.html"
    for arg in sys.argv: 
        if i == 1:
            typeout = sys.argv[i]
        if i == 2:
            filename = sys.argv[i]
        i+=1

        


    with HTML(typeout=typeout, fileName=filename) as doc:
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "hello"
                head += title
            doc += head
        
        with TopLevelTag("body") as body:
            with Tag("h1", klass=("main-text",)) as h1:
                h1.text = "Test"
                body += h1

            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                with Tag("p") as paragraph:
                    paragraph.text = "another test"
                    div += paragraph

                with Tag("img", is_single=True, src="/icon.png", data_image="responsive") as img:
                    div += img

                body += div

            doc += body
        doc.outHTML()
